
# SQM - SQL Manager

SQM (derived from SQL and Manager) is a Django-based, Dockerised database management system (DBMS) designed to streamline the provisioning of MariaDB databases through an API. It eliminates the complexities of encryption and authentication management, allowing developers to focus on building and maintaining their applications without worrying about underlying database credentials.

## Features

SQM offers a suite of features designed to simplify the management of MariaDB databases:

- **User Management:** Easily create users and designate superusers within the application.
- **Database Provisioning:** Seamlessly create databases on an existing MariaDB server with minimal configuration.
- **Database User Management:** Add and manage database users specifically for each database.
- **Air-Gapped Storage:** Critical information is stored in a separate, local Dockerised MariaDB to enhance security and isolation.

## Planned Features

Development is ongoing, and future updates will include:

- **Enhanced Docker Support:** Fixing and improving Docker deployment capabilities.
- **Authentication System Expansion:** Broadening the authentication mechanisms to enhance security and flexibility.
- **Database-Specific API:** Implement APIs for individual database interactions and management.
- **Permission System Expansion:** Develop a more granular permission system to cater to complex organisational needs.
- **Data Encryption:** Implement encryption mechanisms to secure data at rest and in transit.

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- MariaDB or compatible SQL server

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/sqm.git
   cd sqm
   ```

2. **Set up environment variables:**

   Copy the sample `.env.example` to `.env` and modify it according to your environment:

   ```bash
   cp .env.example .env
   ```

3. **Build and run the application:**

   Using Docker Compose, build and deploy your application:

   ```bash
   docker-compose up --build
   ```

### Usage

After deployment, the API can be accessed through the configured port. Use API endpoints to manage users, databases, and permissions.

## Contributing

Contributions to SQM are welcome! If you're looking to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## Licence

This project is licensed under the [GNU GPL v3.9](LICENCE) - see the LICENCE file for details.
