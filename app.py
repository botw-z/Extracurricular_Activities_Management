from flask import jsonify, request, render_template, send_from_directory
from config import app, db
from models import User, ServiceHours
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Serve the HTML file
@app.route('/')
def index():
    return render_template('index.html')

# User authentication routes
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    try:
        user = User.query.filter_by(username=data['username']).first()
        if user and check_password_hash(user.password_hash, data['password']):
            return jsonify({
                'success': True,
                'user_id': user.user_id,
                'role': user.role
            })
        return jsonify({'success': False, 'message': 'Incorrect Username or Password'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    try:
        new_user = User(
            username=data['username'],
            password_hash=generate_password_hash(data['password']),
            email=data['email'],
            role='user'
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Registration successful'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Service hours routes
@app.route('/api/hours', methods=['POST'])
def log_hours():
    data = request.json
    try:
        new_hours = ServiceHours(
            user_id=data['user_id'],
            service_date=datetime.strptime(data['service_date'], '%Y-%m-%d').date(),
            hours_served=data['hours_served'],
            activity_description=data['activity_description'],
            status='pending'
        )
        db.session.add(new_hours)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Hours logged successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/hours/<int:user_id>', methods=['GET'])
def get_user_hours(user_id):
    try:
        hours = ServiceHours.query.filter_by(user_id=user_id).all()
        return jsonify({
            'success': True,
            'hours': [{
                'record_id': h.record_id,
                'service_date': h.service_date.strftime('%Y-%m-%d'),
                'hours_served': float(h.hours_served),
                'activity_description': h.activity_description,
                'status': h.status
            } for h in hours]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/admin/pending', methods=['GET'])
def get_pending_hours():
    try:
        pending = ServiceHours.query.filter_by(status='pending').all()
        return jsonify({
            'success': True,
            'pending_hours': [{
                'record_id': h.record_id,
                'user_id': h.user_id,
                'service_date': h.service_date.strftime('%Y-%m-%d'),
                'hours_served': float(h.hours_served),
                'activity_description': h.activity_description
            } for h in pending]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/admin/verify/<int:record_id>', methods=['PUT'])
def verify_hours(record_id):
    data = request.json
    try:
        hours_record = ServiceHours.query.get_or_404(record_id)
        hours_record.status = data['status']
        hours_record.verified_by = data['admin_id']
        db.session.commit()
        return jsonify({'success': True, 'message': f'Hours {data["status"]} successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 