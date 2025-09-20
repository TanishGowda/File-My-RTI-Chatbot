# RTI Payment Integration Setup Guide

## 1. Database Setup

Run the SQL script to create the RTI applications table:

```sql
-- Copy and paste the contents of rti_applications_table.sql into your Supabase SQL editor
```

## 2. Backend Setup

### Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Environment Variables
Add these to your `backend/.env` file:

```env
# Razorpay Configuration
RAZORPAY_KEY_ID=your_razorpay_key_id_here
RAZORPAY_KEY_SECRET=your_razorpay_key_secret_here

# Email Configuration (Gmail example)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password_here
ADMIN_EMAIL=admin@filemyrti.com
```

### Get Razorpay Credentials
1. Go to [Razorpay Dashboard](https://dashboard.razorpay.com/)
2. Sign up/Login to your account
3. Go to Settings > API Keys
4. Generate API Keys (Test mode for development)
5. Copy Key ID and Key Secret

### Get Gmail App Password
1. Enable 2-Factor Authentication on your Gmail account
2. Go to Google Account Settings > Security
3. Generate an "App Password" for this application
4. Use this password in SMTP_PASSWORD

## 3. Frontend Setup

The frontend is already updated with:
- Razorpay integration
- Payment processing UI
- Success/error handling
- Form validation

## 4. Testing

### Test Payment Flow
1. Fill out the RTI form
2. Attach a Word document
3. Click "Pay with Razorpay" (₹99 fee)
4. Complete payment in Razorpay test mode
5. Verify success message appears
6. Check email notifications

### Test Data
Use Razorpay test card numbers:
- Success: 4111 1111 1111 1111
- Failure: 4000 0000 0000 0002

## 5. Production Deployment

### Razorpay Production
1. Switch to Live mode in Razorpay dashboard
2. Update environment variables with live credentials
3. Update webhook URLs if needed

### Email Configuration
1. Use a professional email service (SendGrid, Mailgun, etc.)
2. Update SMTP settings accordingly
3. Test email delivery

## 6. Features Implemented

✅ **Database Storage**: RTI applications stored in Supabase
✅ **Payment Integration**: Complete Razorpay integration
✅ **Email Notifications**: User and admin email notifications
✅ **File Handling**: Word document attachment and storage
✅ **Form Validation**: Client and server-side validation
✅ **Success Handling**: Payment success confirmation
✅ **Error Handling**: Comprehensive error handling
✅ **Security**: Payment signature verification

## 7. API Endpoints

- `POST /api/v1/rti-applications/create-payment` - Create payment order
- `POST /api/v1/rti-applications/verify-payment` - Verify payment and store data
- `GET /api/v1/rti-applications/applications` - Get user's applications

## 8. Database Schema

The `rti_applications` table stores:
- User information (name, phone, email, address)
- Attached file data (name, content, size)
- Payment information (ID, status)
- Application status and timestamps
