from flask import Flask, request, jsonify, render_template
import cloudinary 

from p2p import app

# upload image 
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        
        if file:
            response=cloudinary.uploader.upload(file, 
                                 upload_preset = "python",
                                 unique_filename = True, 
                                 overwrite=True,
                                 eager=[{"width": 500, "crop": "fill"}])

            image_url = response['eager'][0]['secure_url']
            tags = response['info']['categorization']['aws_rek_tagging']['data'][:3]

            return render_template('index.html', image_url=image_url, tags=tags)

    return render_template('index.html')

# if user deletes account, delete image 
@app.route('/delete', methods=['POST'])
def delete_image():
    if request.method == 'POST':
        image_url = request.form.get('image_url')
        public_id = "/".join(image_url.split('/')[-2:])[:-4]
        result = cloudinary.uploader.destroy(public_id)
        return render_template ('index.html')