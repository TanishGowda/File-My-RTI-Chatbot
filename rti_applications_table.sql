-- Create RTI Applications table
CREATE TABLE rti_applications (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    full_name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    email VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    attached_file_name VARCHAR(255),
    attached_file_data BYTEA,
    attached_file_size INTEGER,
    payment_id VARCHAR(255) UNIQUE, -- Razorpay payment ID
    payment_status VARCHAR(50) DEFAULT 'pending', -- pending, completed, failed
    application_status VARCHAR(50) DEFAULT 'submitted', -- submitted, processing, completed
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for faster queries
CREATE INDEX idx_rti_applications_user_id ON rti_applications(user_id);
CREATE INDEX idx_rti_applications_payment_id ON rti_applications(payment_id);
CREATE INDEX idx_rti_applications_created_at ON rti_applications(created_at);

-- Enable RLS (Row Level Security)
ALTER TABLE rti_applications ENABLE ROW LEVEL SECURITY;

-- Create policy for users to see their own applications
CREATE POLICY "Users can view their own RTI applications" ON rti_applications
    FOR SELECT USING (auth.uid() = user_id);

-- Create policy for users to insert their own applications
CREATE POLICY "Users can insert their own RTI applications" ON rti_applications
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Create policy for users to update their own applications
CREATE POLICY "Users can update their own RTI applications" ON rti_applications
    FOR UPDATE USING (auth.uid() = user_id);

-- Create policy for service role to manage all applications (for admin access)
CREATE POLICY "Service role can manage all RTI applications" ON rti_applications
    FOR ALL USING (auth.role() = 'service_role');
