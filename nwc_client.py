"""
NWC (Nostr Wallet Connect) Client
Implementation based on NIP-47 specification

Reference: https://github.com/nostr-protocol/nips/blob/master/47.md
"""

import asyncio
import json
import hashlib
import secrets
from typing import Optional, Dict, Any, List, Literal
from dataclasses import dataclass
from datetime import datetime
import urllib.parse

# Note: This is a conceptual implementation
# In production, would use actual Nostr and Lightning libraries


@dataclass
class NWCConnectionURI:
    """
    Parse and validate NWC connection URI
    
    Format: nostr+walletconnect://<wallet_pubkey>?relay=<url>&secret=<secret>&lud16=<address>
    
    Parameters:
        wallet_pubkey: 32-byte hex pubkey of wallet service
        relay: WebSocket URL of relay that wallet service listens to
        secret: 32-byte hex random secret for signing and encryption
        lud16: Lightning address (optional)
    """
    wallet_pubkey: str
    relay: str
    secret: str
    lud16: Optional[str] = None
    
    @classmethod
    def from_uri(cls, uri: str) -> 'NWCConnectionURI':
        """Parse NWC connection URI string"""
        if not uri.startswith('nostr+walletconnect://'):
            raise ValueError("Invalid NWC URI: must start with 'nostr+walletconnect://'")
        
        # Extract wallet pubkey
        parts = uri.replace('nostr+walletconnect://', '').split('?')
        wallet_pubkey = parts[0]
        
        # Parse query parameters
        params = urllib.parse.parse_qs(parts[1] if len(parts) > 1 else '')
        
        required = ['relay', 'secret']
        for param in required:
            if param not in params:
                raise ValueError(f"Missing required parameter: {param}")
        
        return cls(
            wallet_pubkey=wallet_pubkey,
            relay=params['relay'][0],
            secret=params['secret'][0],
            lud16=params.get('lud16', [None])[0]
        )
    
    def to_uri(self) -> str:
        """Convert to URI string"""
        params = {
            'relay': self.relay,
            'secret': self.secret
        }
        if self.lud16:
            params['lud16'] = self.lud16
        
        query = urllib.parse.urlencode(params)
        return f"nostr+walletconnect://{self.wallet_pubkey}?{query}"


@dataclass
class NWCEvent:
    """
    NWC Event structure
    
    Event Types (kind):
        13194: Info Event - wallet service capabilities
        23194: Request Event - client request
        23195: Response Event - wallet service response
        23197: Notification Event - wallet notifications
    """
    kind: Literal[13194, 23194, 23195, 23197]
    content: str
    created_at: int
    pubkey: str
    tags: List[List[str]]
    id: Optional[str] = None
    sig: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to Nostr event dict"""
        return {
            'kind': self.kind,
            'content': self.content,
            'created_at': self.created_at,
            'pubkey': self.pubkey,
            'tags': self.tags,
            'id': self.id,
            'sig': self.sig
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NWCEvent':
        """Create from Nostr event dict"""
        return cls(
            kind=data['kind'],
            content=data['content'],
            created_at=data['created_at'],
            pubkey=data['pubkey'],
            tags=data['tags'],
            id=data.get('id'),
            sig=data.get('sig')
        )


@dataclass
class NWCRequest:
    """
    NWC JSON-RPC Request
    
    Common methods:
        pay_invoice: Pay a Lightning invoice
        get_balance: Get wallet balance
        make_invoice: Create a Lightning invoice
        lookup_invoice: Look up invoice status
        list_transactions: List recent transactions
        get_info: Get wallet info
        pay_keysend: Direct payment to pubkey
        make_hold_invoice: Create conditional payment invoice
    """
    method: str
    params: Dict[str, Any]
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps({
            'method': self.method,
            'params': self.params
        })
    
    @classmethod
    def from_json(cls, json_str: str) -> 'NWCRequest':
        """Create from JSON string"""
        data = json.loads(json_str)
        return cls(
            method=data['method'],
            params=data['params']
        )


@dataclass
class NWCResponse:
    """
    NWC JSON-RPC Response
    
    Error codes:
        RATE_LIMITED: Sending too fast
        NOT_IMPLEMENTED: Method not implemented
        INSUFFICIENT_BALANCE: Not enough balance
        QUOTA_EXCEEDED: Quota exceeded
        RESTRICTED: Permission restricted
        UNAUTHORIZED: Unauthorized
        INTERNAL: Internal error
        UNSUPPORTED_ENCRYPTION: Encryption not supported
        OTHER: Other error
    """
    result_type: str
    result: Optional[Dict[str, Any]]
    error: Optional[Dict[str, Any]]
    
    @property
    def success(self) -> bool:
        """Check if response is successful"""
        return self.error is None
    
    @property
    def error_code(self) -> Optional[str]:
        """Get error code if present"""
        return self.error.get('code') if self.error else None
    
    @property
    def error_message(self) -> Optional[str]:
        """Get error message if present"""
        return self.error.get('message') if self.error else None
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps({
            'result_type': self.result_type,
            'result': self.result,
            'error': self.error
        })
    
    @classmethod
    def from_json(cls, json_str: str) -> 'NWCResponse':
        """Create from JSON string"""
        data = json.loads(json_str)
        return cls(
            result_type=data['result_type'],
            result=data.get('result'),
            error=data.get('error')
        )


class NWCPaymentError(Exception):
    """NWC payment error"""
    
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"NWC Error [{code}]: {message}")


class NWCClient:
    """
    NWC Client - Connect to Lightning wallet via Nostr
    
    Usage:
        # Parse connection URI
        uri = NWCConnectionURI.from_uri(nwc_string)
        
        # Create client
        client = NWCClient(uri)
        
        # Get wallet info
        info = await client.get_info()
        
        # Get balance
        balance = await client.get_balance()
        
        # Pay invoice
        result = await client.pay_invoice(invoice="lnbc...")
        
        # Make invoice
        invoice = await client.make_invoice(amount=1000, description="Payment")
    """
    
    def __init__(self, connection_uri: NWCConnectionURI):
        self.connection_uri = connection_uri
        self.wallet_pubkey = connection_uri.wallet_pubkey
        self.relay = connection_uri.relay
        self.secret = connection_uri.secret
        
        # Client state
        self._capabilities: Optional[List[str]] = None
        self._encryption_method: str = "nip04"  # or "nip44"
    
    async def connect(self) -> None:
        """Connect to wallet service and get info"""
        # In production: would establish WebSocket connection to relay
        # For now, just fetch capabilities
        await self._fetch_info()
    
    async def _fetch_info(self) -> None:
        """Fetch wallet service capabilities (kind 13194)"""
        # In production: would query relay for kind 13194 event
        # For now, assume all capabilities are supported
        self._capabilities = [
            "pay_invoice",
            "get_balance",
            "make_invoice",
            "lookup_invoice",
            "list_transactions",
            "get_info",
            "pay_keysend",
            "make_hold_invoice"
        ]
    
    async def _send_request(self, method: str, params: Dict[str, Any]) -> NWCResponse:
        """
        Send request to wallet service
        
        In production, this would:
        1. Create kind 23194 event with encrypted request
        2. Sign event with secret key
        3. Send to relay
        4. Wait for kind 23195 response event
        5. Decrypt and parse response
        """
        # Conceptual implementation
        request = NWCRequest(method=method, params=params)
        
        # Check capability
        if self._capabilities and method not in self._capabilities:
            return NWCResponse(
                result_type=method,
                result=None,
                error={
                    'code': 'NOT_IMPLEMENTED',
                    'message': f'Method {method} not supported by wallet'
                }
            )
        
        # In production: actual relay communication
        # For now: return mock successful response
        return NWCResponse(
            result_type=method,
            result={'status': 'mock_success'},
            error=None
        )
    
    # ========================================
    # Core Methods (8 methods from NIP-47)
    # ========================================
    
    async def get_info(self) -> Dict[str, Any]:
        """
        Get wallet information
        
        Returns:
            {
                'alias': str,          # Wallet name
                'network': str,        # 'mainnet', 'testnet', 'regtest'
                'methods': List[str],  # Supported methods
                'notifications': List[str]  # Supported notifications
            }
        """
        response = await self._send_request('get_info', {})
        
        if not response.success:
            raise NWCPaymentError(response.error_code, response.error_message)
        
        return response.result
    
    async def get_balance(self) -> int:
        """
        Get wallet balance in millisatoshis
        
        Returns:
            Balance in msats (1 sat = 1000 msats)
        """
        response = await self._send_request('get_balance', {})
        
        if not response.success:
            raise NWCPaymentError(response.error_code, response.error_message)
        
        return response.result.get('balance', 0)
    
    async def pay_invoice(self, invoice: str) -> Dict[str, Any]:
        """
        Pay a Lightning invoice
        
        Args:
            invoice: BOLT11 Lightning invoice
        
        Returns:
            {
                'preimage': str,  # Payment preimage (proof of payment)
            }
        
        Raises:
            INSUFFICIENT_BALANCE: Not enough balance
            QUOTA_EXCEEDED: Payment quota exceeded
            INTERNAL: Payment failed
        """
        response = await self._send_request('pay_invoice', {'invoice': invoice})
        
        if not response.success:
            raise NWCPaymentError(response.error_code, response.error_message)
        
        return response.result
    
    async def make_invoice(
        self,
        amount: int,
        description: str = "",
        description_hash: Optional[str] = None,
        expiry: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Create a Lightning invoice
        
        Args:
            amount: Amount in millisatoshis
            description: Invoice description
            description_hash: Hash of description (optional)
            expiry: Expiry time in seconds (optional)
        
        Returns:
            {
                'invoice': str,       # BOLT11 invoice
                'payment_hash': str,  # SHA-256 hash
            }
        """
        params = {
            'amount': amount,
            'description': description
        }
        
        if description_hash:
            params['description_hash'] = description_hash
        if expiry:
            params['expiry'] = expiry
        
        response = await self._send_request('make_invoice', params)
        
        if not response.success:
            raise NWCPaymentError(response.error_code, response.error_message)
        
        return response.result
    
    async def lookup_invoice(
        self,
        payment_hash: Optional[str] = None,
        invoice: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Look up invoice status
        
        Args:
            payment_hash: SHA-256 hash of payment (optional)
            invoice: BOLT11 invoice (optional)
        
        Returns:
            {
                'payment_hash': str,
                'invoice': str,
                'state': str,  # 'pending', 'settled', 'expired', 'failed'
                'amount': int,
                'created_at': int,
                'expires_at': int,
                'settled_at': Optional[int],
                'preimage': Optional[str]
            }
        """
        params = {}
        if payment_hash:
            params['payment_hash'] = payment_hash
        if invoice:
            params['invoice'] = invoice
        
        response = await self._send_request('lookup_invoice', params)
        
        if not response.success:
            raise NWCPaymentError(response.error_code, response.error_message)
        
        return response.result
    
    async def list_transactions(
        self,
        from_timestamp: Optional[int] = None,
        to_timestamp: Optional[int] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        unpaid: Optional[bool] = None,
        type: Optional[str] = None  # 'incoming' or 'outgoing'
    ) -> List[Dict[str, Any]]:
        """
        List transactions
        
        Args:
            from_timestamp: Unix timestamp (optional)
            to_timestamp: Unix timestamp (optional)
            limit: Maximum number of results (optional)
            offset: Offset for pagination (optional)
            unpaid: Include unpaid invoices (optional)
            type: Filter by type (optional)
        
        Returns:
            List of transaction objects
        """
        params = {}
        if from_timestamp:
            params['from'] = from_timestamp
        if to_timestamp:
            params['to'] = to_timestamp
        if limit:
            params['limit'] = limit
        if offset:
            params['offset'] = offset
        if unpaid is not None:
            params['unpaid'] = unpaid
        if type:
            params['type'] = type
        
        response = await self._send_request('list_transactions', params)
        
        if not response.success:
            raise NWCPaymentError(response.error_code, response.error_message)
        
        return response.result.get('transactions', [])
    
    async def pay_keysend(
        self,
        pubkey: str,
        amount: int,
        tlv_records: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Direct payment to node pubkey (no invoice needed)
        
        Args:
            pubkey: Lightning node pubkey
            amount: Amount in millisatoshis
            tlv_records: Custom TLV records (optional)
        
        Returns:
            {
                'preimage': str,
            }
        """
        params = {
            'pubkey': pubkey,
            'amount': amount
        }
        
        if tlv_records:
            params['tlv_records'] = tlv_records
        
        response = await self._send_request('pay_keysend', params)
        
        if not response.success:
            raise NWCPaymentError(response.error_code, response.error_message)
        
        return response.result
    
    async def make_hold_invoice(
        self,
        amount: int,
        payment_hash: str,
        description: str = "",
        expiry: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Create hold invoice (conditional payment)
        
        Use cases:
        - Escrow transactions
        - Conditional payments
        - Atomic swaps
        
        Workflow:
        1. Generate random preimage
        2. Calculate SHA-256 hash = payment_hash
        3. Call make_hold_invoice with payment_hash
        4. Wait for 'hold_invoice_accepted' notification
        5. If accepted: call settle_hold_invoice with preimage
        6. If rejected: call cancel_hold_invoice
        
        Args:
            amount: Amount in millisatoshis
            payment_hash: SHA-256 hash of preimage
            description: Invoice description
            expiry: Expiry in seconds (optional)
        
        Returns:
            {
                'invoice': str,
                'payment_hash': str,
            }
        """
        params = {
            'amount': amount,
            'payment_hash': payment_hash,
            'description': description
        }
        
        if expiry:
            params['expiry'] = expiry
        
        response = await self._send_request('make_hold_invoice', params)
        
        if not response.success:
            raise NWCPaymentError(response.error_code, response.error_message)
        
        return response.result
    
    # ========================================
    # Advanced Methods (not in all wallets)
    # ========================================
    
    async def settle_hold_invoice(self, preimage: str) -> Dict[str, Any]:
        """Settle a hold invoice (release funds)"""
        response = await self._send_request('settle_hold_invoice', {'preimage': preimage})
        
        if not response.success:
            raise NWCPaymentError(response.error_code, response.error_message)
        
        return response.result
    
    async def cancel_hold_invoice(self, payment_hash: str) -> Dict[str, Any]:
        """Cancel a hold invoice (cancel transaction)"""
        response = await self._send_request('cancel_hold_invoice', {'payment_hash': payment_hash})
        
        if not response.success:
            raise NWCPaymentError(response.error_code, response.error_message)
        
        return response.result


# ========================================
# Integration Example for Predyx MCP Server
# ========================================

class PredyxNWCIntegration:
    """
    NWC integration for Predyx MCP Server
    
    Usage in predyx_mcp_server.py:
        
        # Initialize NWC client
        nwc_client = PredyxNWCIntegration(nwc_connection_string)
        
        # Check balance before operation
        balance = await nwc_client.get_balance_msats()
        
        # Process payment
        preimage = await nwc_client.process_payment(invoice, amount_msats)
    """
    
    def __init__(self, nwc_connection_string: Optional[str] = None):
        self.nwc_client: Optional[NWCClient] = None
        
        if nwc_connection_string:
            uri = NWCConnectionURI.from_uri(nwc_connection_string)
            self.nwc_client = NWCClient(uri)
    
    async def initialize(self) -> None:
        """Initialize NWC connection"""
        if self.nwc_client:
            await self.nwc_client.connect()
    
    async def get_balance_sats(self) -> int:
        """Get balance in satoshis"""
        if not self.nwc_client:
            return 0
        
        balance_msats = await self.nwc_client.get_balance()
        return balance_msats // 1000
    
    async def get_balance_msats(self) -> int:
        """Get balance in millisatoshis"""
        if not self.nwc_client:
            return 0
        
        return await self.nwc_client.get_balance()
    
    async def process_payment(self, invoice: str, expected_amount_msats: int) -> str:
        """
        Process payment with balance check
        
        Args:
            invoice: BOLT11 Lightning invoice
            expected_amount_msats: Expected payment amount in msats
        
        Returns:
            Payment preimage (proof of payment)
        
        Raises:
            ValueError: If balance insufficient
            NWCPaymentError: If payment fails
        """
        if not self.nwc_client:
            raise ValueError("NWC client not configured")
        
        # Check balance
        balance = await self.nwc_client.get_balance()
        if balance < expected_amount_msats:
            raise ValueError(
                f"Insufficient balance: {balance} msats < {expected_amount_msats} msats"
            )
        
        # Process payment
        result = await self.nwc_client.pay_invoice(invoice)
        return result['preimage']
    
    async def create_invoice(
        self,
        amount_sats: int,
        description: str,
        expiry_seconds: int = 3600
    ) -> Dict[str, str]:
        """
        Create Lightning invoice
        
        Args:
            amount_sats: Amount in satoshis
            description: Invoice description
            expiry_seconds: Expiry time in seconds (default 1 hour)
        
        Returns:
            {
                'invoice': str,       # BOLT11 invoice
                'payment_hash': str,  # For tracking
            }
        """
        if not self.nwc_client:
            raise ValueError("NWC client not configured")
        
        amount_msats = amount_sats * 1000
        result = await self.nwc_client.make_invoice(
            amount=amount_msats,
            description=description,
            expiry=expiry_seconds
        )
        
        return {
            'invoice': result['invoice'],
            'payment_hash': result['payment_hash']
        }


# ========================================
# Example Usage
# ========================================

async def example_usage():
    """Example: Using NWC client"""
    
    # 1. Parse connection URI
    nwc_string = "nostr+walletconnect://69effe...?relay=wss://relay.damus.io&secret=..."
    uri = NWCConnectionURI.from_uri(nwc_string)
    
    # 2. Create client
    client = NWCClient(uri)
    
    # 3. Connect
    await client.connect()
    
    # 4. Get info
    info = await client.get_info()
    print(f"Wallet: {info['alias']}")
    print(f"Network: {info['network']}")
    print(f"Methods: {info['methods']}")
    
    # 5. Get balance
    balance_msats = await client.get_balance()
    balance_sats = balance_msats // 1000
    print(f"Balance: {balance_sats} sats")
    
    # 6. Pay invoice
    invoice = "lnbc1000n1pj9y20..."
    try:
        result = await client.pay_invoice(invoice)
        print(f"Payment successful! Preimage: {result['preimage']}")
    except NWCPaymentError as e:
        print(f"Payment failed: {e.code} - {e.message}")
    
    # 7. Create invoice
    new_invoice = await client.make_invoice(
        amount=5000,  # 5 sats in msats
        description="Predyx market analysis",
        expiry=3600  # 1 hour
    )
    print(f"Invoice: {new_invoice['invoice']}")
    print(f"Payment hash: {new_invoice['payment_hash']}")


if __name__ == "__main__":
    # Run example
    asyncio.run(example_usage())
