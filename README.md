# Kash - Digital Wallet and Virtual Card Platform

Kash is a comprehensive digital wallet and virtual card platform designed to provide seamless financial services to users. This project includes features such as user management, KYC verification, virtual card issuance and management, transaction processing, and more. 

I wrote a technical overview of the codebase [here](https://nelsonkamga.com/tech/kash.html).

## Key Features

- User Management: Create and manage user profiles with secure authentication.
- KYC Verification: Implement Know Your Customer processes for user verification.
- Virtual Cards: Issue and manage virtual cards for online transactions.
- Transaction Processing: Handle various types of transactions including payments and payouts.
- Referral System: Implement a user referral program with rewards.
- Promo Codes: Manage promotional codes for user benefits.
- Notifications: Send push notifications to users for important updates.

## Tech Stack

- Backend: Django with Django REST Framework
- Database: PostgreSQL
- Payment Processing: Integration with various payment gateways
- Push Notifications: OneSignal SDK

## Getting Started

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up the database and run migrations: `python manage.py migrate`
4. Start the development server: `python manage.py runserver`

## Project Structure

- `kash/`: Main project directory
  - `abstract/`: Base models and utilities
  - `auth/`: Authentication related models
  - `card/`: Virtual card management
  - `earning/`: Earnings tracking
  - `invite/`: Invitation and referral system
  - `kyc/`: KYC document management
  - `notification/`: User notification system
  - `payout/`: Payout request handling
  - `promo/`: Promotional code management
  - `transaction/`: Transaction processing
  - `user/`: User profile management
  - `xlib/`: Utility functions and external integrations

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
