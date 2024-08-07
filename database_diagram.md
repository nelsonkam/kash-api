erDiagram
    User ||--|| UserProfile : "profile"
    KYCDocument ||--|| UserProfile : "profile"
    Notification ||--|| UserProfile : "profile"
    VirtualCard ||--|| UserProfile : "profile"
    FundingHistory ||--|| VirtualCard : "card"
    WithdrawalHistory ||--|| VirtualCard : "card"
    Earning ||--o{ Transaction : "transaction"
    InviteCode ||--|| UserProfile : "inviter"
    InviteCode ||--o| UserProfile : "invited"
    Referral ||--|| UserProfile : "referred"
    Referral }|--|| UserProfile : "referrer"
    Transaction ||--o| User : "initiator"
    PromoCode }|--o{ UserProfile : "applied_to"
    VerificationMethod }|--|| UserProfile : "profile"
    AdminPayoutRequest ||--o| Transaction : "transaction"
    Topup ||--o| Transaction : "transaction"
    CardAction ||--|| VirtualCard : "card"
    Rate ||--o{ Topup : "topup"

    User {
        string username
        string name
        string phone_number
        string avatar_url
    }
    UserProfile {
        string kashtag
        array device_ids
        string avatar_url
        string referral_code
        int promo_balance
    }
    KYCDocument {
        string doc_url
        string document_type
        string selfie_url
        string status
        string rejection_reason
    }
    Notification {
        int object_id
        string title
        string description
        datetime sent_at
    }
    VirtualCard {
        string external_id
        boolean is_active
        boolean is_permablocked
        string permablock_reason
        string nickname
        string category
        string last_4
        string provider_name
    }
    FundingHistory {
        string txn_ref
        money amount
        string status
        int retries
        boolean is_funding
    }
    WithdrawalHistory {
        string txn_ref
        money amount
        string status
    }
    Earning {
        money amount
        string operation
        string txn_ref
    }
    InviteCode {
        string code
        datetime used_at
    }
    Referral {
        datetime rewarded_at
    }
    Transaction {
        int object_id
        string gateway
        string reference
        string refund_reference
        string service_reference
        string status
        money amount
        money discount
        datetime discount_accounted_at
        string name
        string phone
        string transaction_type
        string service_message
        datetime last_status_checked
        string provider_name
    }
    PromoCode {
        string code
        int value
        datetime expires_at
        boolean is_valid
    }
    VerificationMethod {
        string type
        string value
        boolean is_verified
    }
    AdminPayoutRequest {
        string code
        string phone
        string gateway
        int amount
    }
    Topup {
        string code
        int amount
        string ngn_payin_status
        string xof_txn_status
        string usd_txn_status
        string xof_txn_ref
        boolean is_canceled
    }
    CardAction {
        string code
        boolean is_confirmed
        string action_type
        int amount
    }
    Rate {
        string code
        decimal value
    }
