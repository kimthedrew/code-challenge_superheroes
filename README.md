# code-challenge-superheroes
# Superheroes API

A Flask RESTful API for tracking heroes and their superpowers, with a React frontend.

## Features

- RESTful endpoints for heroes and powers
- Many-to-many relationships between heroes and powers
- Data validation
- SQLite database with migrations
- React frontend integration

## Models

### Hero
- `id`: Integer (Primary Key)
- `name`: String
- `super_name`: String
- Relationships:
  - Many-to-many with `Power` through `HeroPower`

### Power
- `id`: Integer (Primary Key)
- `name`: String
- `description`: String (minimum 20 characters)
- Relationships:
  - Many-to-many with `Hero` through `HeroPower`

### HeroPower
- `id`: Integer (Primary Key)
- `strength`: String (must be 'Strong', 'Weak', or 'Average')
- `hero_id`: Integer (Foreign Key)
- `power_id`: Integer (Foreign Key)

## API Endpoints

### Heroes
- `GET /heroes` - Get all heroes
- `GET /heroes/:id` - Get a specific hero with their powers

### Powers
- `GET /powers` - Get all powers
- `GET /powers/:id` - Get a specific power
- `PATCH /powers/:id` - Update a power's description

### HeroPowers
- `POST /hero_powers` - Create a new hero-power association

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Phase-4-Code-Challenge-Superheroes-062023/code-challenge
