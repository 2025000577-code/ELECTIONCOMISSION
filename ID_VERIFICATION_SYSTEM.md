# 🆔 Identity Verification System

## Overview
The voting system now includes a comprehensive identity verification system using ID card proof uploads. This ensures only verified users can vote, preventing fraud and maintaining election integrity.

## Features

### 1. User Registration with ID Proof
- Users must provide:
  - Full name
  - Email address
  - Username
  - National ID or Voter ID number
  - ID card photo (front side)
  - Password

### 2. Admin Verification Dashboard
- Dedicated verification interface at `/voting-admin/verify-users/`
- View pending verifications
- Review ID card proofs
- Approve or reject users
- Track verification history

### 3. Security Features
- Users cannot vote until verified by admin
- ID card numbers are unique (no duplicates)
- Verification status tracked with timestamp
- Audit trail of who verified each user
- Secure image storage

## How It Works

### For Users:
1. **Register** with ID proof
2. **Wait** for admin verification (24-48 hours)
3. **Login** after verification
4. **Vote** once verified

### For Admins:
1. **Login** to admin dashboard
2. **Click** "Verify Users" button
3. **Review** ID card proofs
4. **Verify** or reject each user
5. **Track** verification history

## Admin Access

### Verification Dashboard
- URL: `http://YOUR_IP:8000/voting-admin/verify-users/`
- Shows:
  - Pending verifications count
  - List of unverified users
  - Recently verified users
  - User details and ID proofs

### Verification Process
1. Click "View ID" to see ID card proof
2. Verify checklist:
   - ✓ ID card is clear and readable
   - ✓ Name matches registration
   - ✓ ID number matches
   - ✓ ID appears authentic
   - ✓ No duplicate registration
3. Click "Verify User" or "Reject & Delete"

## Database Changes

### New Fields in User Model:
```python
id_card_number      # Unique ID number
id_card_proof       # Image file
is_verified         # Boolean status
verified_at         # Timestamp
verified_by         # Admin who verified
```

### Migration Applied:
- `0002_user_id_card_number_user_id_card_proof_and_more.py`

## File Structure

### New Templates:
- `templates/voting/verification_pending.html` - User waiting page
- `templates/voting/verify_users.html` - Admin verification list
- `templates/voting/view_id_proof.html` - ID proof viewer

### Updated Files:
- `voting/models.py` - Added verification fields
- `voting/forms.py` - Added ID upload to registration
- `voting/views.py` - Added verification logic
- `voting/urls.py` - Added verification routes
- `templates/voting/admin_dashboard.html` - Added verification button

## Security Enhancements

### Fraud Prevention:
1. **Unique ID Numbers** - No duplicate registrations
2. **Admin Approval** - Manual verification required
3. **Audit Trail** - Track who verified whom
4. **Image Proof** - Visual verification of identity
5. **Verification Check** - Users must be verified to vote

### Logging:
- All verification actions logged
- Security events tracked
- Admin actions recorded

## Usage Instructions

### First Time Setup:
```bash
# Install Pillow for image handling
pip install Pillow==10.1.0

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

### Admin Workflow:
1. Navigate to admin dashboard
2. Click "Verify Users" button
3. Review each pending user:
   - Check ID card photo
   - Verify name and ID number
   - Approve or reject
4. Users can vote after approval

### User Experience:
1. Register with ID proof
2. See "Verification Pending" page
3. Wait for admin approval
4. Login and vote once verified

## Benefits

### For Election Integrity:
- ✅ Prevents fake registrations
- ✅ Ensures one person = one vote
- ✅ Verifiable voter identity
- ✅ Audit trail for compliance

### For Administrators:
- ✅ Easy verification interface
- ✅ Bulk verification capability
- ✅ Clear audit history
- ✅ Reject suspicious accounts

### For Users:
- ✅ Secure registration process
- ✅ Clear verification status
- ✅ Protected voting rights
- ✅ Transparent process

## Technical Details

### Image Storage:
- Location: `media/id_proofs/`
- Format: Any image format (JPG, PNG, etc.)
- Security: Accessible only to admins

### Database Constraints:
- ID card number: Unique, max 50 characters
- Verification status: Boolean, default False
- Verified timestamp: Auto-set on approval

### Access Control:
- Unverified users: Cannot vote
- Verified users: Can vote once
- Admins: Can verify users
- Public: Cannot access ID proofs

## Future Enhancements

### Possible Additions:
- Email notifications on verification
- SMS verification codes
- Automated ID verification (OCR)
- Bulk verification tools
- Verification expiry dates
- Re-verification requirements

## Troubleshooting

### Common Issues:

**Issue: Image not uploading**
- Solution: Ensure Pillow is installed
- Check file size limits
- Verify media folder permissions

**Issue: Users can't vote after verification**
- Solution: Check is_verified field in database
- Ensure admin clicked "Verify" button
- Check for session issues

**Issue: ID proof not displaying**
- Solution: Check MEDIA_URL in settings
- Verify file path is correct
- Ensure static files are served

## Summary

The identity verification system adds a crucial security layer to the voting system, ensuring only legitimate users can participate in elections. With admin oversight and ID proof verification, the system maintains high integrity while remaining user-friendly.

---

**System Status:** ✅ Fully Implemented and Tested
**Migration Status:** ✅ Applied Successfully
**Ready for Use:** ✅ Yes
