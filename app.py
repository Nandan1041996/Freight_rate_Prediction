import os
import shutil
import zipfile
import io
import pandas as pd
import numpy as np
import logging
import secrets
from werkzeug.utils import secure_filename
from functions import fraight_rate_calculation
from flask import Flask, request, flash, redirect, send_file, render_template, url_for,jsonify

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)  # Set logging level to ERROR or higher
handler = logging.FileHandler('error.log')  # Log errors to a file
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Initialize app
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

result_df = None

@app.route('/upload_files', methods=['POST'])
def upload_files():

    global result_df

    if 'current_fraight_file' not in request.files or \
       'destination_fraight_file' not in request.files or \
       'old_fraight_file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    current_fraight_file = request.files['current_fraight_file']
    destination_fraight_file = request.files['destination_fraight_file']
    old_fraight_file = request.files['old_fraight_file']
    perc_increase = request.form.get('perc_increase')

    if not (allowed_file(current_fraight_file.filename) and allowed_file(destination_fraight_file.filename) and allowed_file(old_fraight_file.filename)):
        flash('Invalid file format. Please upload Excel files only.')
        return redirect(request.url)

    # Check if files are provided
    if current_fraight_file.filename == '' or destination_fraight_file.filename == '' or old_fraight_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename1 = secure_filename(current_fraight_file.filename)
    filename2 = secure_filename(destination_fraight_file.filename)
    filename3 = secure_filename(old_fraight_file.filename)

    current_fraight_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
    destination_fraight_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
    old_fraight_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename3))

    file_path1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
    file_path2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
    file_path3 = os.path.join(app.config['UPLOAD_FOLDER'], filename3)

    # Process percentage increase (optional)
    if perc_increase:
        perc_increase = float(perc_increase)

    result_df = fraight_rate_calculation(file_path1, file_path2, file_path3, perc_increase)

    if not isinstance(result_df,pd.DataFrame):
        return  render_template('error_page.html', error_message=str(result_df))
    
    else:
        for file in [file_path1,file_path2,file_path3]:
            os.remove(file)
        # Render the template with the filtered DataFrame
        return render_template('result_display.html', filtered_df=result_df.to_html(classes='table table-striped'))


@app.route('/suggested_rate',methods=['GET'])
def suggested_rate_calculation():
    try:
        suggested_rate_in_perc = float(request.args.get('suggested_freight_rate'))
        if suggested_rate_in_perc == '':
            return jsonify({'error': 'No selected file'}), 400
        result_df['Final_Price'] = result_df['Direct Road Freight']+(result_df['Direct Road Freight'] * (suggested_rate_in_perc+0.1))

        return render_template('result_display.html', filtered_df=result_df.to_html(classes='table table-striped'))
    except Exception as e:
        return e

if __name__ == '__main__':
    app.run(debug=True)



# import os
# import shutil
# import zipfile
# import io
# import pandas as pd
# import numpy as np 
# import logging
# import secrets
# from werkzeug.utils import secure_filename
# from functions import fraight_rate_calculation
# from flask import Flask, request, flash, redirect, send_file, render_template, url_for

# # Initialize logger
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.ERROR)  # Set logging level to ERROR or higher
# handler = logging.FileHandler('error.log')  # Log errors to a file
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)

# # Initialize app
# app = Flask(__name__)
# app.secret_key = secrets.token_hex(16)

# # Upload folder
# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/upload_files', methods=['POST'])
# def upload_files():
#     if 'current_fraightrate_file' not in request.files or 'old_fraightrate_file' not in request.files or 'destination_fraightrate_file' not in request.files:
#         flash('No file part')
#         return redirect(request.url)
#     print('in')
#     current_fraightrate_file = request.files['current_fraight_file']
#     destination_fraight_file = request.files['destination_fraight_file']
#     old_fraightrate_file = request.files['old_fraightrate_file']

#     if not (allowed_file(current_fraightrate_file.filename) and allowed_file(destination_fraight_file.filename) and allowed_file(old_fraightrate_file.filename)):
#         flash('Invalid file format. Please upload Excel files only.')
#         return redirect(request.url)
    
#     filename1 = secure_filename(current_fraightrate_file.filename)
#     filename2 = secure_filename(destination_fraight_file.filename)
#     filename3 = secure_filename(old_fraightrate_file.filename)

#     current_fraightrate_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
#     destination_fraight_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
#     old_fraightrate_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename3))

#     file_path1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
#     file_path2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
#     file_path3 = os.path.join(app.config['UPLOAD_FOLDER'], filename3)
    


#     try:
#         result_df = fraight_rate_calculation(file_path1, file_path2, file_path3)
#         if not isinstance(result_df, pd.DataFrame):
#             return render_template('error_page.html', error_message=str(result_df))
#         else:
#             return render_template('result_display.html', filtered_df=result_df.to_html(classes='table table-striped'))
#     except Exception as e:
#         logger.error("Error occurred during file processing: %s", str(e))
#         flash("An error occurred during file processing.")
#         return redirect(url_for('index'))

# if __name__ == '__main__':
#     app.run(debug=True)



# # import os
# # import shutil
# # import zipfile
# # import io
# # import pandas as pd
# # import numpy as np 
# # import logging
# # import secrets
# # import logging
# # from werkzeug.utils import secure_filename
# # from functions import fraight_rate_calculation
# # from flask import Flask, request, flash, redirect, send_file, render_template, url_for
# # # perc_increase = diesel_inc_dec_percentage(92,91.86)


# # # Initialize logger
# # logger = logging.getLogger(__name__)
# # logger.setLevel(logging.ERROR)  # Set logging level to ERROR or higher
# # handler = logging.FileHandler('error.log')  # Log errors to a file
# # formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# # handler.setFormatter(formatter)
# # logger.addHandler(handler)

# # # initialize app
# # app = Flask(__name__)
# # app.secret_key = secrets.token_hex(16)

# # # upload filder
# # UPLOAD_FOLDER = 'uploads'
# # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # ALLOWED_EXTENSIONS = {'xlsx', 'xls'}


# # # initialize app
# # app = Flask(__name__)
# # app.secret_key = secrets.token_hex(16)


# # @app.route('/')
# # def index():
# #     return render_template('index.html')


# # def allowed_file(filename):
# #     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# # @app.route('/upload', methods=['POST'])
# # def submit_button():
# #     if 'current_fraight_file' not in request.files or 'old_fraight_file' not in request.files or 'destination_fraight_file' not in request.files:
# #         flash('No file part')
# #         return redirect(request.url)
    
# #     current_fraightrate_file = request.files['current_fraight_file']
# #     destination_fraight_file = request.files['destination_fraight_file']
# #     old_fraightrate_file = request.files['old_fraightrate_file']
# #     perc_increase = request.args.get('percentage_increase/decrease')


# #     if not (allowed_file(current_fraightrate_file.filename) and allowed_file(destination_fraight_file.filename) and allowed_file(old_fraightrate_file.filename)):
# #         flash('Invalid file format. Please upload Excel files only.')
# #         return redirect(request.url)
    

# #     filename1 = secure_filename(current_fraightrate_file.filename)
# #     filename2 = secure_filename(destination_fraight_file.filename)
# #     filename3 = secure_filename(old_fraightrate_file.filename)

# #     current_fraightrate_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
# #     destination_fraight_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
# #     old_fraightrate_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename3))

# #     file_path1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
# #     file_path2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
# #     file_path3 = os.path.join(app.config['UPLOAD_FOLDER'], filename3)

# #     result_df = fraight_rate_calculation(file_path1,file_path2,file_path3,perc_increase)
# #     if not isinstance(result_df,pd.DataFrame):
# #             return render_template('error_page.html', error_message=str(result_df))
    
# #     else:
# #         # Render the template with the filtered DataFrame
# #         return render_template('result_display.html', filtered_df=result_df.to_html(classes='table table-striped'))




# # if __name__ == '__main__':
# #     app.run(debug=True)