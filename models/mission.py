from ..db import db

class Mission(db.Model):
    mission_id = db.Column(db.Integer, primary_key=True)
    mission_date = db.Column(db.Date)
    theater_of_operations = db.Column(db.String(100))
    country = db.Column(db.String(100))
    air_force = db.Column(db.String(100))
    unit_id = db.Column(db.String(100))
    aircraft_series = db.Column(db.String(100))
    callsign = db.Column(db.String(100))
    mission_type = db.Column(db.String(100))
    takeoff_base = db.Column(db.String(255))
    takeoff_location = db.Column(db.String(255))
    takeoff_latitude = db.Column(db.String(15))
    takeoff_longitude = db.Column(db.Numeric(10, 6))
    target_id = db.Column(db.String(100))
    altitude_hundreds_of_feet = db.Column(db.Numeric(7, 2))
    airborne_aircraft = db.Column(db.Numeric(4, 1))
    attacking_aircraft = db.Column(db.Integer)
    bombing_aircraft = db.Column(db.Integer)
    aircraft_returned = db.Column(db.Integer)
    aircraft_failed = db.Column(db.Integer)
    aircraft_damaged = db.Column(db.Integer)
    aircraft_lost = db.Column(db.Integer)
    high_explosives = db.Column(db.String(255))
    high_explosives_type = db.Column(db.String(255))
    high_explosives_weight_pounds = db.Column(db.String(25))
    high_explosives_weight_tons = db.Column(db.Numeric(10, 2))
    incendiary_devices = db.Column(db.String(255))
    incendiary_devices_type = db.Column(db.String(255))
    incendiary_devices_weight_pounds = db.Column(db.Numeric(10, 2))
    incendiary_devices_weight_tons = db.Column(db.Numeric(10, 2))
    fragmentation_devices = db.Column(db.String(255))
    fragmentation_devices_type = db.Column(db.String(255))
    fragmentation_devices_weight_pounds = db.Column(db.Numeric(10, 2))
    fragmentation_devices_weight_tons = db.Column(db.Numeric(10, 2))
    total_weight_pounds = db.Column(db.Numeric(10, 2))
    total_weight_tons = db.Column(db.Numeric(10, 2))
    time_over_target = db.Column(db.String(8))
    bomb_damage_assessment = db.Column(db.String(255))
    source_id = db.Column(db.String(100))

    def to_dict(self):
        return {
            'mission_id': self.mission_id,
            'mission_date': str(self.mission_date),  # Converting date to string for JSON
            'theater_of_operations': self.theater_of_operations,
            'country': self.country,
            'air_force': self.air_force,
            'unit_id': self.unit_id,
            'aircraft_series': self.aircraft_series,
            'callsign': self.callsign,
            'mission_type': self.mission_type,
            'takeoff_base': self.takeoff_base,
            'takeoff_location': self.takeoff_location,
            'takeoff_latitude': self.takeoff_latitude,
            'takeoff_longitude': float(self.takeoff_longitude) if self.takeoff_longitude else None,
            'target_id': self.target_id,
            'altitude_hundreds_of_feet': float(
                self.altitude_hundreds_of_feet) if self.altitude_hundreds_of_feet else None,
            'airborne_aircraft': float(self.airborne_aircraft) if self.airborne_aircraft else None,
            'attacking_aircraft': self.attacking_aircraft,
            'bombing_aircraft': self.bombing_aircraft,
            'aircraft_returned': self.aircraft_returned,
            'aircraft_failed': self.aircraft_failed,
            'aircraft_damaged': self.aircraft_damaged,
            'aircraft_lost': self.aircraft_lost,
            'high_explosives': self.high_explosives,
            'high_explosives_type': self.high_explosives_type,
            'high_explosives_weight_pounds': self.high_explosives_weight_pounds,
            'high_explosives_weight_tons': float(
                self.high_explosives_weight_tons) if self.high_explosives_weight_tons else None,
            'incendiary_devices': self.incendiary_devices,
            'incendiary_devices_type': self.incendiary_devices_type,
            'incendiary_devices_weight_pounds': float(
                self.incendiary_devices_weight_pounds) if self.incendiary_devices_weight_pounds else None,
            'incendiary_devices_weight_tons': float(
                self.incendiary_devices_weight_tons) if self.incendiary_devices_weight_tons else None,
            'fragmentation_devices': self.fragmentation_devices,
            'fragmentation_devices_type': self.fragmentation_devices_type,
            'fragmentation_devices_weight_pounds': float(
                self.fragmentation_devices_weight_pounds) if self.fragmentation_devices_weight_pounds else None,
            'fragmentation_devices_weight_tons': float(
                self.fragmentation_devices_weight_tons) if self.fragmentation_devices_weight_tons else None,
            'total_weight_pounds': float(self.total_weight_pounds) if self.total_weight_pounds else None,
            'total_weight_tons': float(self.total_weight_tons) if self.total_weight_tons else None,
            'time_over_target': self.time_over_target,
            'bomb_damage_assessment': self.bomb_damage_assessment,
            'source_id': self.source_id
        }