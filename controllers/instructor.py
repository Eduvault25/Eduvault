from flask import request, render_template, redirect, url_for, session
from bson import ObjectId
from datetime import datetime
import cloudinary.uploader
import json
from app import app, db, courses_collection


# Instructor Dashboard
@app.route('/instructor/dashboard')
def instructor_dashboard():
    if session.get("role") != "instructor":
        return redirect(url_for("signin_signup"))

    instructor_id = session.get("user_id")
    courses = list(courses_collection.find({"instructor_id": instructor_id}))

    for course in courses:
        course["_id"] = str(course["_id"])  # Convert ObjectId to string

    user = db.users.find_one({"_id": ObjectId(instructor_id)})
    
    return render_template("instructor/instructor_dash.html", courses=courses, user=user,str=str)

@app.route("/instructor/my-courses")
def instructor_my_courses():
    if session.get("role") != "instructor":
        return redirect(url_for("signin_signup"))

    instructor_id = session.get("user_id")
    courses = list(courses_collection.find({"instructor_id": ObjectId(instructor_id)}))

    for course in courses:
        course["_id"] = str(course["_id"])

        # Parse structure if stored as a string
        if isinstance(course.get("structure"), str):
            try:
                course["structure"] = json.loads(course["structure"])
            except Exception as e:
                print(f"❌ Error parsing structure for course {course['_id']}: {e}")
                course["structure"] = {"modules": []}

    return render_template("instructor/my_courses.html", courses=courses, page="courses")

@app.route('/instructor/create-course', methods=['GET', 'POST'])
def create_course():
    if session.get("role") != "instructor":
        return redirect(url_for("signin_signup"))

    if request.method == 'POST':
        try:
            user_id = session.get("user_id")
            if not user_id:
                raise Exception("User not logged in")

            # === Step 1: Form Inputs ===
            title = request.form.get('course_title')
            description = request.form.get('description')
            difficulty = request.form.get('difficulty')
            category = request.form.get('category')
            language = request.form.get('language')
            prerequisites = request.form.get('prerequisites')
            learning_objectives = request.form.get('learning_objectives')
            thumbnail = request.files.get('thumbnail')
            structure_json = request.form.get('structure_json')
            submit_type = request.form.get('submit_type')

            if not structure_json:
                raise Exception("Structure data is missing.")

            try:
                structure_data = json.loads(structure_json)
            except Exception as e:
                raise Exception("Invalid structure JSON: " + str(e))

            # === Step 2: Upload Thumbnail ===
            thumbnail_url = ""
            if thumbnail:
                upload_result = cloudinary.uploader.upload(thumbnail)
                thumbnail_url = upload_result.get("secure_url")

            # === Step 3: Upload Topic Files ===
            for module in structure_data.get("modules", []):
                for chapter in module.get("chapters", []):
                    for topic in chapter.get("topics", []):
                        topic_id = topic.get("topic_id")
                        content_type = topic.get("content_type")

                        file_field = f"topic_file_{topic_id}"
                        uploaded_file = request.files.get(file_field)

                        # Handle link or file content
                        if content_type == "link":
                            topic["content_url"] = topic.get("content", "")
                        elif uploaded_file:
                            # Determine Cloudinary resource type
                            if content_type == 'video':
                                resource_type = 'video'
                            elif content_type in ['pdf', 'zip', 'other']:
                                resource_type = 'raw'
                            elif content_type == 'image':
                                resource_type = 'image'
                            else:
                                resource_type = 'auto'

                            # Upload to Cloudinary
                            upload_result = cloudinary.uploader.upload(uploaded_file, resource_type=resource_type)
                            topic["content_url"] = upload_result.get("secure_url")
                        else:
                            topic["content_url"] = ""

                        # Clean up redundant 'content'
                        topic.pop("content", None)

            # === Step 4: Prepare Final Document ===
            course_data = {
                "title": title,
                "description": description,
                "difficulty": difficulty,
                "category": category,
                "language": language,
                "prerequisites": prerequisites,
                "learning_objectives": learning_objectives,
                "thumbnail_url": thumbnail_url,
                "structure": structure_data,
                "instructor_id": ObjectId(user_id),
                "status": "draft" if submit_type == "draft" else "published",
                "created_at": datetime.utcnow()
            }

            # === Step 5: Insert into DB ===
            courses_collection.insert_one(course_data)

            return redirect(url_for('instructor_my_courses'))

        except Exception as e:
            print("❌ Error during course creation:", str(e))
            return render_template('instructor/create_course.html', error="Something went wrong: " + str(e))

    return render_template('instructor/create_course.html')


#course details
@app.route("/instructor/course/<course_id>")
def view_course(course_id):
    course = courses_collection.find_one({"_id": ObjectId(course_id)})
    if not course:
        return "Course not found", 404
    return render_template("instructor/view_course.html", course=course)
