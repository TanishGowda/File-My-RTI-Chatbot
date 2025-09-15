# FileMyRTI AI Chatbot - Project Analysis & Documentation

## Project Overview

**FileMyRTI** is a React-based web application that provides an AI-powered chatbot service for drafting Right to Information (RTI) applications. The application helps Indian citizens create legally compliant RTI drafts and offers optional paid filing services.

### Key Information
- **Project Name**: rti-chatbot-ui
- **Version**: 0.1.0
- **Technology Stack**: React 19.1.1, React Router DOM 7.8.2, Supabase 2.57.4
- **Target Users**: Indian citizens seeking to file RTI applications
- **Company**: Ranazonai Technologies

## Architecture & Dependencies

### Core Dependencies
- **React 19.1.1**: Modern React with latest features
- **React Router DOM 7.8.2**: Client-side routing
- **Supabase 2.57.4**: Backend-as-a-Service for authentication and data
- **React Scripts 5.0.1**: Build and development tools
- **Testing Libraries**: Jest, React Testing Library for unit testing

### Project Structure
```
src/
├── components/          # Reusable UI components
│   ├── ChatWindow.jsx   # Main chat interface
│   ├── Sidebar.jsx      # Navigation and conversation list
│   └── ThemeToggle.jsx  # Dark/light mode toggle
├── pages/              # Route-based page components
│   ├── AuthPage.jsx     # Login page
│   ├── SignupPage.jsx   # Registration page
│   ├── ChatPage.jsx     # Main chat interface
│   ├── FileRTIPage.jsx  # RTI filing service page
│   ├── TermsPage.jsx    # Terms and conditions
│   └── PrivacyPage.jsx  # Privacy policy
├── styles/             # CSS styling files
│   ├── authstyles.css   # Authentication page styles
│   ├── chatstyles.css   # Chat interface styles
│   └── styles.css       # Global styles
└── App.jsx             # Main application component
```

## Application Workflow

### 1. Entry Point & Routing
- **Default Route**: `/` redirects to `/auth`
- **Authentication**: `/auth` and `/signup` for user management
- **Main Application**: `/chat` for the chatbot interface
- **Services**: `/file-rti` for paid RTI filing
- **Legal Pages**: `/terms` and `/privacy` for compliance

### 2. User Authentication Flow

#### Login Page (`/auth`)
- **Purpose**: User authentication entry point
- **Features**:
  - Email/password login form
  - Google OAuth integration (UI only)
  - Link to signup page
  - Terms and Privacy policy links
- **UI Elements**:
  - FileMyRTI logo and branding
  - Clean, centered form layout
  - Responsive design with 3D box effect

#### Signup Page (`/signup`)
- **Purpose**: New user registration
- **Features**:
  - Full name, email, password fields
  - Google OAuth signup option
  - Link back to login page
  - Legal compliance links
- **UI Elements**: Similar to login page with registration-specific fields

### 3. Main Chat Interface (`/chat`)

#### ChatPage Component
- **State Management**:
  - `darkMode`: Theme toggle state
  - `sidebarOpen`: Sidebar visibility control
  - `conversations`: Array of chat conversations
  - `activeId`: Currently selected conversation

#### Key Features
- **Multi-conversation Support**: Users can create and switch between multiple chat sessions
- **Real-time Chat**: Interactive messaging with the AI bot
- **Theme Support**: Dark/light mode toggle
- **Responsive Design**: Collapsible sidebar for mobile/tablet views

#### Conversation Management
- **Default Conversation**: Pre-loaded with welcome message
- **New Chat Creation**: Generates unique conversation IDs
- **Message Handling**: Supports both user and bot messages
- **Conversation Switching**: Click to switch between different chats

### 4. Chat Interface Components

#### Sidebar Component
- **Branding**: FileMyRTI logo and branding
- **Navigation**:
  - "File RTI With Us" button (redirects to `/file-rti`)
  - "New chat" button for creating conversations
  - Conversation list with titles
- **User Account**:
  - Guest user display
  - Account menu with profile, settings, and theme toggle
  - Dark/light mode switching

#### ChatWindow Component
- **Landing State**: 
  - Animated "Welcome to FileMyRTI" typing effect
  - Interactive input field with call-to-action
  - Feature preview icons (attach, download, voice - coming soon)
- **Active Chat State**:
  - Message history display
  - User and bot message bubbles
  - Input field with send functionality
- **Input Features**:
  - Auto-resizing textarea
  - Enter key to send (Shift+Enter for new line)
  - Placeholder icons for future features

### 5. RTI Filing Service (`/file-rti`)

#### FileRTIPage Component
- **Purpose**: Paid RTI filing service interface
- **Form Fields**:
  - Full Name
  - Email
  - Mobile Number
  - Address (textarea)
- **Payment Integration**:
  - Razorpay payment button (UI only)
  - ₹199 pricing display
  - Terms and Privacy policy links

### 6. Legal Compliance Pages

#### Terms Page (`/terms`)
- **Comprehensive Terms & Conditions** covering:
  - Service nature and limitations
  - User eligibility (Indian citizens only)
  - User responsibilities and restrictions
  - Drafting limitations and disclaimers
  - Filing service terms
  - Refund and cancellation policies
  - Liability limitations
  - Intellectual property rights
  - Governing law (India, Hyderabad jurisdiction)

#### Privacy Page (`/privacy`)
- **Privacy Policy** covering:
  - Data collection practices
  - Information usage
  - Data sharing policies
  - Security measures
  - User rights
  - Data retention policies
  - Contact information

## Styling Architecture

### CSS Organization
- **authstyles.css**: Authentication pages styling
- **chatstyles.css**: Chat interface and sidebar styling
- **styles.css**: Global styles and base components

### Design System
- **Color Scheme**: 
  - Light mode: White backgrounds with dark text
  - Dark mode: Black/dark backgrounds with light text
- **Typography**: Segoe UI font family
- **Components**: Modern, clean design with subtle shadows and rounded corners
- **Responsive**: Mobile-first approach with flexible layouts

### Key Styling Features
- **Glassmorphism**: Backdrop blur effects on sidebar and chat window
- **Smooth Transitions**: 0.3s transitions for theme changes
- **Interactive Elements**: Hover effects and visual feedback
- **Accessibility**: Proper contrast ratios and focus states

## Technical Implementation

### State Management
- **Local State**: React hooks (useState, useEffect, useMemo)
- **No Global State**: Simple component-level state management
- **Props Drilling**: Data passed down through component hierarchy

### Routing
- **React Router DOM**: Client-side routing with BrowserRouter
- **Route Protection**: No authentication guards implemented
- **Navigation**: Programmatic navigation and Link components

### Data Flow
1. **App.jsx**: Main router configuration
2. **ChatPage**: Manages conversation state and chat logic
3. **Sidebar**: Handles conversation selection and user actions
4. **ChatWindow**: Manages message display and input handling

## Current Limitations & Future Enhancements

### Current State
- **UI Only**: No backend integration for authentication or chat
- **Mock Data**: Conversations stored in local state
- **No Persistence**: Data lost on page refresh
- **No AI Integration**: Chat responses not implemented

### Planned Features (UI Ready)
- **File Attachment**: Attach button in chat input
- **Download Drafts**: Download button for RTI drafts
- **Voice Input**: Microphone button for voice messages
- **Payment Processing**: Razorpay integration for RTI filing

### Technical Debt
- **Authentication**: No actual login/signup functionality
- **Data Persistence**: No database integration
- **Error Handling**: Limited error states and validation
- **Testing**: No test coverage implemented

## Business Model

### Service Offerings
1. **Free Service**: AI-powered RTI draft generation
2. **Paid Service**: Complete RTI filing on behalf of users (₹199)
3. **Self-Service**: Users can download and file drafts themselves

### Target Market
- **Primary**: Indian citizens seeking RTI information
- **Use Cases**: Government transparency, legal compliance, information access
- **Geographic**: India-focused (RTI Act 2005 compliance)

## Security & Compliance

### Data Protection
- **Privacy Policy**: Comprehensive data handling guidelines
- **Terms of Service**: Clear usage terms and limitations
- **User Rights**: Data deletion and access rights defined

### Legal Compliance
- **RTI Act 2005**: Service designed for Indian RTI requirements
- **Data Retention**: 90-day retention policy
- **Jurisdiction**: Hyderabad, Telangana, India

## Conclusion

The FileMyRTI AI Chatbot represents a well-structured React application with a clear focus on RTI (Right to Information) services for Indian citizens. The application demonstrates modern React development practices with a clean component architecture, responsive design, and comprehensive legal compliance documentation. While currently a UI prototype, the foundation is solid for implementing backend services, AI integration, and payment processing to create a fully functional RTI assistance platform.

The project shows attention to user experience, legal compliance, and technical architecture, making it ready for production development with proper backend integration and AI service implementation.
