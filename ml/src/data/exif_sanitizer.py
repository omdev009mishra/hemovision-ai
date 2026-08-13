"""
HemoVision — EXIF Metadata Privacy Sanitizer
Strips PII EXIF fields (GPS coordinates, serial numbers, hardware IDs) while preserving research metadata.
"""

from typing import Dict, Any, Tuple, Set


FORBIDDEN_EXIF_TAGS: Set[str] = {
    "GPSInfo", "GPSLatitude", "GPSLongitude", "GPSAltitude", "GPSTimeStamp",
    "DeviceSerialNumber", "BodySerialNumber", "CameraSerialNumber",
    "LensSerialNumber", "SerialNumber", "OwnerName", "Artist", "Author",
    "InternalSerialNumber", "MacAddress", "IMEI", "IPAddress"
}

ALLOWED_EXIF_TAGS: Set[str] = {
    "Make", "Model", "LensMake", "LensModel", "LensSpecification",
    "DateTime", "DateTimeOriginal", "DateTimeDigitized",
    "ExifImageWidth", "ExifImageHeight", "ExposureTime", "FNumber",
    "ISOSpeedRatings", "FocalLength", "Flash", "Orientation"
}


class EXIFSanitizer:
    """Sanitizes EXIF metadata dictionaries to enforce patient privacy."""

    @staticmethod
    def sanitize_metadata(raw_metadata: Dict[str, Any]) -> Tuple[Dict[str, Any], bool]:
        """
        Sanitizes EXIF metadata dictionary.

        Returns:
            Tuple of (sanitized_metadata_dict, contains_stripped_pii_flag)
        """
        sanitized = {}
        had_forbidden = False

        for k, v in raw_metadata.items():
            k_str = str(k)
            if k_str in FORBIDDEN_EXIF_TAGS or "GPS" in k_str or "Serial" in k_str:
                had_forbidden = True
                continue

            if k_str in ALLOWED_EXIF_TAGS or k_str.startswith("camera_") or k_str.startswith("phone_"):
                sanitized[k_str] = v

        return sanitized, had_forbidden
