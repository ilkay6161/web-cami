from datetime import datetime
from database import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with blog posts
    blog_posts = db.relationship('BlogPost', backref='author', lazy='dynamic', cascade="all, delete-orphan")
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.String(200))
    image_url = db.Column(db.String(255))
    published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign key to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'<BlogPost {self.title}>'


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Page {self.title}>'

# Nachrichtensystem für Admin-Bereich
class AdminMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_name = db.Column(db.String(100), nullable=False)
    sender_email = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    received_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    admin_response = db.Column(db.Text)
    response_date = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<AdminMessage {self.subject}>'

# Veranstaltungssystem
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_date = db.Column(db.DateTime, nullable=False)
    event_time = db.Column(db.String(20))  # z.B. "14:30"
    location = db.Column(db.String(200))
    is_recurring = db.Column(db.Boolean, default=False)
    recurrence_type = db.Column(db.String(50))  # weekly, monthly, etc.
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @property
    def is_past(self):
        """Prüft ob Veranstaltung bereits vorbei ist"""
        return self.event_date < datetime.utcnow()
    
    def __repr__(self):
        return f'<Event {self.title}>'


# Erweiterte Klassenbuch-Modelle für professionelle Anwendung
class Subject(db.Model):
    """Fächer-Modell"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    short_name = db.Column(db.String(10), nullable=False)
    color = db.Column(db.String(7), default='#007bff')  # Hex-Farbcode
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Beziehungen
    lessons = db.relationship('Lesson', backref='subject', lazy='dynamic')
    teacher_subjects = db.relationship('TeacherSubject', backref='subject', lazy='dynamic')
    grades = db.relationship('Grade', backref='subject', lazy='dynamic')
    
    def __repr__(self):
        return f'<Subject {self.name}>'


class Teacher(db.Model):
    """Lehrer-Modell"""
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20))
    employee_id = db.Column(db.String(20), unique=True)
    hire_date = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Beziehungen
    teacher_subjects = db.relationship('TeacherSubject', backref='teacher', lazy='dynamic')
    lessons = db.relationship('Lesson', backref='teacher', lazy='dynamic')
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f'<Teacher {self.full_name}>'


class TeacherSubject(db.Model):
    """Zuordnung Lehrer zu Fächern"""
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)  # Hauptfach des Lehrers
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class TimeSlot(db.Model):
    """Zeitslots für Stundenplan"""
    id = db.Column(db.Integer, primary_key=True)
    period_number = db.Column(db.Integer, nullable=False)  # Stundennummer (1, 2, 3, ...)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    is_break = db.Column(db.Boolean, default=False)
    break_duration = db.Column(db.Integer, default=0)  # Pause in Minuten
    
    # Beziehungen
    schedule_entries = db.relationship('ScheduleEntry', backref='time_slot', lazy='dynamic')
    
    def __repr__(self):
        return f'<TimeSlot {self.period_number}: {self.start_time}-{self.end_time}>'


class ScheduleEntry(db.Model):
    """Stundenplan-Eintrag"""
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class_room.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    time_slot_id = db.Column(db.Integer, db.ForeignKey('time_slot.id'), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0=Montag, 1=Dienstag, ...
    room = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
    valid_from = db.Column(db.Date, default=datetime.utcnow().date())
    valid_until = db.Column(db.Date)
    
    def __repr__(self):
        return f'<ScheduleEntry {self.day_of_week}-{self.time_slot.period_number}>'


class ClassRoom(db.Model):
    """Erweiterte Klassen mit zusätzlichen Informationen"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    school_year = db.Column(db.String(9), nullable=False)
    grade_level = db.Column(db.Integer)  # Klassenstufe
    section = db.Column(db.String(5))  # Klassenbezeichnung (a, b, c, ...)
    class_teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    max_students = db.Column(db.Integer, default=30)
    room_number = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Beziehungen
    students = db.relationship('Student', backref='class_room', lazy='dynamic')
    lessons = db.relationship('Lesson', backref='class_room', lazy='dynamic')
    schedule_entries = db.relationship('ScheduleEntry', backref='class_room', lazy='dynamic')
    class_teacher = db.relationship('Teacher', backref='class_rooms')
    
    @property
    def full_name(self):
        return f"{self.name} ({self.school_year})"
    
    def __repr__(self):
        return f'<ClassRoom {self.full_name}>'


class Student(db.Model):
    """Erweiterte Schüler-Informationen"""
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True)  # Schülernummer
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date)
    gender = db.Column(db.String(1))  # M/F/D
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    parent_contact = db.Column(db.String(200))
    emergency_contact = db.Column(db.String(200))
    medical_info = db.Column(db.Text)
    enrollment_date = db.Column(db.Date, default=datetime.utcnow().date())
    is_active = db.Column(db.Boolean, default=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class_room.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Beziehungen
    attendances = db.relationship('Attendance', backref='student', lazy='dynamic')
    grades = db.relationship('Grade', backref='student', lazy='dynamic')
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        if self.birth_date:
            today = datetime.utcnow().date()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None
    
    def __repr__(self):
        return f'<Student {self.full_name}>'


class Lesson(db.Model):
    """Unterrichtseinheit/Stunde"""
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    period = db.Column(db.Integer, nullable=False)  # Stundennummer
    class_id = db.Column(db.Integer, db.ForeignKey('class_room.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    topic = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    homework = db.Column(db.Text)
    materials = db.Column(db.Text)
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='planned')  # planned, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Beziehungen
    attendances = db.relationship('Attendance', backref='lesson', lazy='dynamic')
    
    def __repr__(self):
        return f'<Lesson {self.date} - {self.topic}>'


class Attendance(db.Model):
    """Erweiterte Anwesenheit"""
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    status = db.Column(db.String(20), default='present')  # present, absent, late, excused
    arrival_time = db.Column(db.Time)
    excuse_reason = db.Column(db.Text)
    excuse_document = db.Column(db.String(255))  # Dateiname der Entschuldigung
    excuse_verified = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)
    recorded_by = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    
    def __repr__(self):
        return f'<Attendance {self.student.full_name} - {self.status}>'


class GradeType(db.Model):
    """Bewertungstypen (Klausur, Test, mündlich, etc.)"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    short_name = db.Column(db.String(10), nullable=False)
    weight = db.Column(db.Float, default=1.0)  # Gewichtung für Gesamtnote
    color = db.Column(db.String(7), default='#28a745')
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    
    # Beziehungen
    grades = db.relationship('Grade', backref='grade_type', lazy='dynamic')
    
    def __repr__(self):
        return f'<GradeType {self.name}>'


class Grade(db.Model):
    """Noten/Bewertungen"""
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    grade_type_id = db.Column(db.Integer, db.ForeignKey('grade_type.id'), nullable=False)
    
    # Bewertung
    points = db.Column(db.Float)  # Erreichte Punkte
    max_points = db.Column(db.Float)  # Maximale Punkte
    grade_value = db.Column(db.Float)  # Note (1.0 - 6.0)
    percentage = db.Column(db.Float)  # Prozent
    
    # Details
    exam_date = db.Column(db.Date, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    comments = db.Column(db.Text)
    
    # Metadaten
    weight = db.Column(db.Float, default=1.0)  # Individuelle Gewichtung
    is_published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @property
    def grade_letter(self):
        """Konvertiert Notenwert zu Buchstabennote"""
        if not self.grade_value:
            return None
        if self.grade_value <= 1.5:
            return 'A'
        elif self.grade_value <= 2.5:
            return 'B'
        elif self.grade_value <= 3.5:
            return 'C'
        elif self.grade_value <= 4.5:
            return 'D'
        elif self.grade_value <= 5.5:
            return 'E'
        else:
            return 'F'
    
    def __repr__(self):
        return f'<Grade {self.student.full_name} - {self.subject.name}: {self.grade_value}>'


class AbsenceReport(db.Model):
    """Fehlzeiten-Berichte"""
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    is_excused = db.Column(db.Boolean, default=False)
    excuse_document = db.Column(db.String(255))
    reported_by = db.Column(db.String(100))  # Wer hat gemeldet (Eltern, Arzt, etc.)
    verified_by = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def duration_days(self):
        """Berechnet die Anzahl der Fehltage"""
        return (self.end_date - self.start_date).days + 1
    
    def __repr__(self):
        return f'<AbsenceReport {self.student.full_name}: {self.start_date} - {self.end_date}>'