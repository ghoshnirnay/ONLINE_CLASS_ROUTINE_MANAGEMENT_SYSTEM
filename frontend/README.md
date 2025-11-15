# Online Class Routine Management System

A comprehensive web-based platform for managing class schedules in educational institutions with role-based access for administrators, faculty, and students.

## Features

- **Role-Based Access Control**: Separate dashboards for Admin, Faculty, and Students
- **Automated Routine Management**: Create and manage class schedules with conflict detection
- **Real-Time Notifications**: Instant alerts for schedule changes
- **Search & Filter**: Advanced filtering by department, subject, faculty, room, and date
- **Calendar Views**: Weekly schedule view with today's highlight
- **Class Swap Requests**: Faculty can request class swaps
- **Multi-Department Support**: Manage multiple departments and their schedules
- **Configurable Time Slots**: Flexible time slot configuration for classes and labs
- **Routine History**: Track all schedule changes
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## Technology Stack

- **Frontend**: Nuxt.js 2 (Vue.js framework)
- **Backend**: Supabase (PostgreSQL database with authentication)
- **Styling**: Custom CSS with design system
- **Authentication**: Supabase Auth with email/password

## Database Schema

The system includes the following tables:
- `profiles` - User profiles with role-based access
- `departments` - Academic departments
- `subjects` - Course/subject information
- `rooms` - Classroom and lab information
- `time_slots` - Configurable time periods
- `routines` - Main schedule entries
- `routine_history` - Version control for schedules
- `notifications` - Real-time user notifications
- `swap_requests` - Faculty class swap requests
- `feedback` - User feedback and suggestions

## Getting Started

### Prerequisites

- Node.js 14+ and npm/yarn
- Supabase account (database is pre-configured)

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm run start
```

### Environment Variables

The `.env` file contains your Supabase credentials:
- `VITE_SUPABASE_URL` - Your Supabase project URL
- `VITE_SUPABASE_ANON_KEY` - Your Supabase anonymous key

## User Roles

### Admin
- Full system access
- Create and manage routines
- Manage departments, subjects, rooms, and time slots
- Review swap requests
- View all user feedback
- Access to system statistics

### Faculty
- View personal class schedule
- Request class swaps
- View department routines
- Receive notifications for schedule changes

### Student
- View department class schedule
- Filter and search schedules
- Export schedules
- Receive notifications for routine updates

## Getting Started as a New User

1. Visit the application homepage
2. Click "Create Account"
3. Fill in your details:
   - Full Name
   - Email
   - Password
   - Select your role (Admin/Faculty/Student)
   - Select your department
4. After registration, login with your credentials
5. You'll be redirected to your role-specific dashboard

## Sample Data

The system comes pre-populated with:
- 3 Departments (Computer Science, Mathematics, Physics)
- 7 Rooms (Classrooms, Labs, Auditorium)
- 12 Time Slots (Class periods and lab sessions)
- 12 Subjects across all departments

## Key Features by Module

### Routine Management
- Create new class schedules
- Assign faculty, room, time slot, and subject
- Set effective dates
- Automatic conflict detection
- Version history tracking

### Notification System
- Real-time notifications for schedule changes
- Notification types: routine changes, swap requests, system alerts
- Mark as read functionality
- Mark all as read option

### Search & Filter
- Filter by department
- Filter by day of week
- Search by subject, faculty, or room
- Calendar view with weekly layout

### Conflict Detection
- Prevents double-booking of faculty
- Prevents room conflicts
- Time slot overlap detection

## Project Structure

```
├── assets/css/          # Global styles
├── components/          # Vue components
│   ├── AdminDashboard.vue
│   ├── FacultyDashboard.vue
│   ├── StudentDashboard.vue
│   ├── Header.vue
│   └── WeeklySchedule.vue
├── layouts/             # Layout components
├── middleware/          # Route middleware (auth)
├── pages/              # Application routes
│   ├── index.vue       # Landing page
│   ├── login.vue       # Login page
│   ├── register.vue    # Registration
│   ├── dashboard.vue   # Main dashboard
│   ├── routines.vue    # Routines listing
│   ├── notifications.vue
│   └── manage/         # Admin management pages
├── plugins/            # Nuxt plugins (Supabase)
└── nuxt.config.js     # Nuxt configuration
```

## Security Features

- Row Level Security (RLS) enabled on all tables
- Role-based access policies
- Authenticated-only routes
- Secure password authentication
- Profile data validation

## Future Enhancements

- PDF/Excel export functionality
- Email notifications
- Bulk routine import
- Academic calendar integration
- Attendance tracking
- Room availability checker
- Mobile app
- Advanced analytics and reports

## License

This project is created for educational purposes.
