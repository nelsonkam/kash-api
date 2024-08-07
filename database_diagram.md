erDiagram
    KYCDocument ||--|| UserProfile : "profile"
    Notification ||--|| UserProfile : "profile"
    VirtualCard ||--|| UserProfile : "profile"
    FundingHistory ||--|| VirtualCard : "card"
    WithdrawalHistory ||--|| VirtualCard : "card"
    Earning {
        string operation
        string txn_ref
    }
    InviteCode ||--|| UserProfile : "inviter"
    InviteCode ||--o| UserProfile : "invited"
    Referral ||--|| UserProfile : "referred"
    Referral }|--|| UserProfile : "referrer"
    Transaction ||--o| User : "initiator"
    PromoCode }|--o{ UserProfile : "applied_to"

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
