from enum import Enum
from typing import Optional

class RoomType(Enum):
    STANDARD = "standard"
    LARGE = "large"
    SUITE = "suite"
    BALCONY = "balcony"

class RoomStatus(Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    CLEANING = "cleaning"
    OUT_OF_ORDER = "out_of_order"

class Room:
    def __init__(self, room_number: int, floor: int, room_type: RoomType, price_per_night: float):
        self.room_number = room_number
        self.floor = floor
        self.room_type = room_type
        self.price_per_night = price_per_night
        self.status = RoomStatus.AVAILABLE
    
    # Getters
    def get_room_number(self) -> int:
        return self.room_number
    
    def get_floor(self) -> int:
        return self.floor
    
    def get_room_type(self) -> RoomType:
        return self.room_type
    
    def get_status(self) -> RoomStatus:
        return self.status
    
    def get_price_per_night(self) -> float:
        return self.price_per_night
    
    # Status management
    def mark_occupied(self):
        self.status = RoomStatus.OCCUPIED
    
    def mark_cleaning(self):
        self.status = RoomStatus.CLEANING
    
    def mark_available(self):
        self.status = RoomStatus.AVAILABLE
    
    def mark_out_of_order(self):
        self.status = RoomStatus.OUT_OF_ORDER
    
    def is_available(self) -> bool:
        return self.status == RoomStatus.AVAILABLE

class Guest:
    def __init__(self, guest_id: int, name: str, email: str, phone: str):
        self.guest_id = guest_id
        self.name = name
        self.email = email
        self.phone = phone
    
    # Getters
    def get_guest_id(self) -> int:
        return self.guest_id
    
    def get_name(self) -> str:
        return self.name
    
    def get_email(self) -> str:
        return self.email
    
    def get_phone(self) -> str:
        return self.phone
    
    # Setters (for updates)
    def update_email(self, email: str):
        self.email = email
    
    def update_phone(self, phone: str):
        self.phone = phone


from datetime import datetime, date
from typing import List, Optional
import uuid

# New classes added below:

class ReservationStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CHECKED_IN = "checked_in"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Reservation:
    def __init__(self, reservation_id: str, guest: Guest, room: Room, 
                 check_in_date: date, check_out_date: date, total_price: float):
        self.reservation_id = reservation_id
        self.guest = guest
        self.room = room
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.total_price = total_price
        self.status = ReservationStatus.CONFIRMED
    
    def get_reservation_id(self) -> str:
        return self.reservation_id
    
    def get_guest(self) -> Guest:
        return self.guest
    
    def get_room(self) -> Room:
        return self.room
    
    def get_check_in_date(self) -> date:
        return self.check_in_date
    
    def get_check_out_date(self) -> date:
        return self.check_out_date
    
    def get_status(self) -> ReservationStatus:
        return self.status
    
    def cancel(self):
        self.status = ReservationStatus.CANCELLED

class ReservationManager:
    def __init__(self):
        self.reservations: List[Reservation] = []
        self.rooms: List[Room] = []  # Or inject this as dependency
    
    def make_reservation(self, guest: Guest, room_type: RoomType, 
                        check_in_date: date, check_out_date: date) -> Optional[Reservation]:
        """Create a new reservation if room is available"""
        
        # Validate dates
        if check_in_date >= check_out_date:
            raise ValueError("Check-in date must be before check-out date")
        
        if check_in_date < date.today():
            raise ValueError("Check-in date cannot be in the past")
        
        # Find available room
        available_room = self._find_available_room(room_type, check_in_date, check_out_date)
        if not available_room:
            return None  # No rooms available
        
        # Calculate total price
        nights = (check_out_date - check_in_date).days
        total_price = nights * available_room.get_price_per_night()
        
        # Create reservation
        reservation_id = str(uuid.uuid4())
        reservation = Reservation(
            reservation_id=reservation_id,
            guest=guest,
            room=available_room,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            total_price=total_price
        )
        
        self.reservations.append(reservation)
        return reservation
    
    def find_reservation_by_id(self, reservation_id: str) -> Optional[Reservation]:
        """Find reservation by ID"""
        for reservation in self.reservations:
            if reservation.get_reservation_id() == reservation_id:
                return reservation
        return None
    
    def find_reservations_by_guest(self, guest_id: int) -> List[Reservation]:
        """Find all reservations for a guest"""
        guest_reservations = []
        for reservation in self.reservations:
            if reservation.get_guest().get_guest_id() == guest_id:
                guest_reservations.append(reservation)
        return guest_reservations
    
    def cancel_reservation(self, reservation_id: str) -> bool:
        """Cancel a reservation"""
        reservation = self.find_reservation_by_id(reservation_id)
        if reservation and reservation.get_status() in [ReservationStatus.PENDING, ReservationStatus.CONFIRMED]:
            reservation.cancel()
            return True
        return False
    
    def _find_available_room(self, room_type: RoomType, check_in: date, check_out: date) -> Optional[Room]:
        """Find an available room of specified type for given dates"""
        for room in self.rooms:
            if (room.get_room_type() == room_type and 
                self._is_room_available(room, check_in, check_out)):
                return room
        return None
    
    def _is_room_available(self, room: Room, check_in: date, check_out: date) -> bool:
        """Check if room is available for given date range"""
        for reservation in self.reservations:
            if (reservation.get_room().get_room_number() == room.get_room_number() and
                reservation.get_status() in [ReservationStatus.CONFIRMED, ReservationStatus.CHECKED_IN] and
                self._dates_overlap(reservation.get_check_in_date(), reservation.get_check_out_date(), 
                                  check_in, check_out)):
                return False
        return True
    
    def _dates_overlap(self, start1: date, end1: date, start2: date, end2: date) -> bool:
        """Check if two date ranges overlap"""
        return start1 < end2 and start2 < end1

class CheckInOutManager:
    def __init__(self, reservation_manager: ReservationManager):
        self.reservation_manager = reservation_manager
    
    def check_in(self, reservation_id: str) -> bool:
        reservation = self.reservation_manager.find_reservation_by_id(reservation_id)
        if reservation and reservation.get_status() == ReservationStatus.CONFIRMED:
            reservation.status = ReservationStatus.CHECKED_IN
            reservation.get_room().mark_occupied()
            return True
        return False
    
    def check_out(self, reservation_id: str) -> bool:
        reservation = self.reservation_manager.find_reservation_by_id(reservation_id)
        if reservation and reservation.get_status() == ReservationStatus.CHECKED_IN:
            reservation.status = ReservationStatus.COMPLETED
            reservation.get_room().mark_cleaning()
            return True
        return False

class HotelSystem:
    def __init__(self):
        self.reservation_manager = ReservationManager()
        self.checkin_manager = CheckInOutManager(self.reservation_manager)
    
    def add_room(self, room: Room):
        self.reservation_manager.rooms.append(room)
    
    def make_reservation(self, guest: Guest, room_type: RoomType, check_in: date, check_out: date):
        return self.reservation_manager.make_reservation(guest, room_type, check_in, check_out)
    
    def check_in_guest(self, reservation_id: str):
        return self.checkin_manager.check_in(reservation_id)
    
    def check_out_guest(self, reservation_id: str):
        return self.checkin_manager.check_out(reservation_id)