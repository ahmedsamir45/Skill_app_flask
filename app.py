from webapp import create_app



app = create_app()



# __init__.py or app.py
import os
from flask import current_app

with app.app_context():
    # Ensure the profile_pics directory exists
    if not os.path.exists(os.path.join(current_app.root_path, 'static/profile_pics')):
        os.makedirs(os.path.join(current_app.root_path, 'static/profile_pics'))


    

if __name__ == "__main__" :
    app.run(debug=False,port=5000,host="0.0.0.0")
