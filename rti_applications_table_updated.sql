-- Updated RTI Applications Table Schema
-- This version stores file data as TEXT (base64) instead of BYTEA

-- Drop the existing table if it exists
DROP TABLE IF EXISTS rti_applications;

-- Create the updated table
CREATE TABLE rti_applications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    full_name TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    email TEXT NOT NULL,
    address TEXT NOT NULL,
    attached_file_name TEXT NOT NULL,
    attached_file_data TEXT NOT NULL, -- Store file as base64 string
    attached_file_size INT NOT NULL,
    razorpay_order_id TEXT NOT NULL,
    razorpay_payment_id TEXT,
    razorpay_signature TEXT,
    payment_status TEXT NOT NULL DEFAULT 'pending',
    amount_paid INT NOT NULL, -- Amount in paise
    currency TEXT NOT NULL DEFAULT 'INR',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE rti_applications ENABLE ROW LEVEL SECURITY;

-- Create RLS policies
CREATE POLICY "Users can view their own RTI applications." ON rti_applications
FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own RTI applications." ON rti_applications
FOR INSERT WITH CHECK (auth.uid() = user_id);

-- No update or delete policies for users, as applications are immutable after submission

-- Create indexes for better performance
CREATE INDEX idx_rti_applications_user_id ON rti_applications(user_id);
CREATE INDEX idx_rti_applications_payment_id ON rti_applications(razorpay_payment_id);
CREATE INDEX idx_rti_applications_created_at ON rti_applications(created_at);
