# 🎬 UWEFlix Cinema Booking System

An integrated cinema booking system developed for the UWEFlix student cinema. This project streamlines ticket purchasing for students and university clubs while providing administrative features for cinema staff and account managers. It emphasizes usability, accessibility, secure payments, and sustainability.

## 📌 Features

### 🎟️ Ticket Booking
- **Advance and On-site Purchases**: Students and general customers can purchase tickets in advance or at the cinema.
- **Showings Selection**: Browse available showings by date, including film title, age rating, duration, and a short trailer description.
- **Flexible Ticket Types**: Choose from student, child, or adult tickets.
- **Real-time Availability**: System checks for seat availability before confirming bookings.
- **Secure Payments**: Integrates with the existing Payment Transaction System for processing credit or debit card payments.
- **Email Confirmations**: Sends booking confirmations to customers via email.

### 🏫 Club Management
- **Club Registration**: Cinema managers can register university clubs and their representatives, capturing essential details.
- **Bulk Ticket Purchases**: Clubs can purchase blocks of tickets at discounted rates.
- **Account Payments**: Allows clubs to make payments via account, with unique account numbers and discount rates.

### 🎥 Film and Screen Management
- **Film Catalog Management**: Add, update, or delete film details, including title, age rating, duration, and trailer descriptions.
- **Screen Management**: Add new screens with capacity details and manage showings across different screens and times.
- **Schedule Management**: Ensure no overlapping showings and manage repeated screenings efficiently.

### 📊 Account Management
- **Account Creation and Modification**: Account managers can create new accounts for clubs and amend existing ones.
- **Monthly Statements**: Generate and view end-of-month account statements detailing debit and credit transactions.
- **Data Validation**: Ensures data integrity with input constraints and validations.

### 🌐 Accessibility and Compliance
- **User Interface Quality**: Designed with a focus on usability for both UK and international students, including those with visual impairments.
- **Multilingual Support**: Potential for supporting multiple languages to cater to a diverse user base.
- **GDPR Compliance**: Ensures user data privacy and security.
- **Sustainability**: Promotes a green agenda by reducing paper usage and optimizing resource consumption.

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- pip (Python package installer)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/jakubkarafa/uweflix-cinema-booking-system.git
   cd uweflix-cinema-booking-system
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Apply migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

5. **Access the application**:
   Open your browser and navigate to `http://localhost:8000`

## 🧪 Testing

To run tests and ensure everything is working correctly:

```bash
python manage.py test
```
