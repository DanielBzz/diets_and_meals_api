# diets_and_meals_api

The Diets and Meals API application is a microservices-based system designed to efficiently manage meals, dishes, and diets data. It is composed of four independent services, each serving a specific purpose.

## About

The application comprises four services, namely:

**1. Meals Service:** 
- Creates and stores dishes and meals (by selecting 3 dishes from the database).
- Allows retrieval, update, and deletion of dishes and meals.
- Computes real-time nutrition facts for each dish and meal using data from a nutrition API.

**2. Diet Service:**
- Manages diet data, specifically the maximum nutrition facts for a meal.
- Supports retrieval, update, and deletion of diet information.
- Enables requests to the Meals API with a diet query parameter, returning meals conforming to the specified diet.

**3. Database Service:** 
Implements with MySQL to persistently store all application data.

**4. Reverse-Proxy Service (NGINX):** 
Routes incoming requests to the appropriate server, ensuring seamless communication between services.

## Architecture

![צילום מסך 2023-10-09 000138](https://github.com/DanielBzz/diets_and_meals_api/assets/90978006/5a674cc8-7fe0-46fb-833b-3de82187b975)

## Key features

**Microservices Architecture:** Each service operates independently, promoting modularity and scalability.

**Dockerized Containers:** Utilizes Docker for containerization, allowing for consistent deployment across different environments.

**HTTP Requests and Reverse Proxy:** Demonstrates effective communication between microservices via HTTP requests. NGINX serves as a reverse proxy to direct requests to the correct service.


## License
This project is licensed under the MIT License.
