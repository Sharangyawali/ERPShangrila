# -*- coding: utf-8 -*-
from odoo import http,fields
from odoo.http import request
import base64
from datetime import datetime,timedelta


class EmployeeDashboard(http.Controller):

    @http.route('/personal_registration', auth='user', website=True)
    def employee_signup_template(self, **kw):
        user_id=request.env.user.id
        request_details=request.env['employee.registration.request'].sudo().search([('user_id','=',user_id)])
        print(request_details)
        # department=request.env['hr.department'].search([])
        # department_list=[]
        # for dp in department:
        #     department_list.append({
        #         'id':dp.id,
        #         'name':dp.name
        #     })
        return request.render("employee_dashboard.employee_submit_page", {'details':request_details,'i':0})

    @http.route('/otp_page', auth='public', website=True)
    def render_otp_page(self, **kw):
        return request.render("employee_dashboard.employee_signin_template", {})

    @http.route('/submit/personal_registration',methods=['POST'], csrf=False, auth='user', website=True)
    def SubmitRegistrationRequest(self,**post):
        user_id=request.env.user.id
        user=request.env['employee.registration.request'].search([('user_id','=',request.env.user.id)])
        # this below is for the personal information
        user_name=post.get('user_name')
        permanent_address=post.get('permanent_address')
        temporary_address=post.get('temporary_address')
        citizenship_no=post.get('citizenship_no')
        pan=post.get('pan')
        passport_no=post.get('passport_no')
        user_email=post.get('user_email')
        phone=post.get('phone')
        gender=post.get('gender')
        photo = request.httprequest.files.get('photo')
        photo_read = photo.read() if photo else False
        photo_encode = base64.b64encode(photo_read) if photo_read else False

        department = post.get('department')
        position = post.get('position')
        age = post.get('age')

        upload_pan = request.httprequest.files.get('upload_pan')
        upload_pan_read = upload_pan.read() if upload_pan else False
        upload_pan_encoded = base64.b64encode(upload_pan_read) if upload_pan_read else False

        citizenship_file = request.httprequest.files.get('identification_file')
        identification_file_read = citizenship_file.read() if citizenship_file else False
        identification_file_encoded = base64.b64encode(identification_file_read) if identification_file_read else False

        # this below is for the family information
        father_name=post.get('father_name')
        mother_name=post.get('mother_name')
        marital_status=post.get('marital_status')
        partner_name=post.get('partner_name')
        number_of_children=post.get('number_of_children')
        grandfather_name=post.get('grandfather_name')

        # study experience related info
        graduation_year=request.httprequest.form.getlist('graduation_year')
        institution_name=request.httprequest.form.getlist('institution_name')
        certificate_level=request.httprequest.form.getlist('certification_level')
        field_of_study=request.httprequest.form.getlist('field_of_study')
        academic_certificates = []
        for i in range(len(certificate_level)):
            certificate_files = []
            file_key = f'academic_certificates_{i}'
            print(file_key)
            if f'academic_certificates_{i}' in request.httprequest.files:
                file = request.httprequest.files.getlist(file_key)
                if file and any(file):
                    for f in file:
                        f_content = base64.b64encode(f.read())
                        # academic_certificates[i].append({'file':f_content})
                        certificate_files.append({'file': f_content})
                academic_certificates.append(certificate_files)
        print(academic_certificates)
        worked_position=request.httprequest.form.getlist('worked_position')
        duration_of_employment=request.httprequest.form.getlist('duration_of_employment')
        company_name=request.httprequest.form.getlist('company_name')
        exit_reason=request.httprequest.form.getlist('exit_reason')
        related_skills=post.get('related_skills')

        cv_encoded = base64.b64encode(request.httprequest.files.get('cv').read()) if request.httprequest.files.get('cv') else False
        cover_letter = base64.b64encode(request.httprequest.files.get('cover_letter').read()) if request.httprequest.files.get('cover_letter') else False
        professional_certifications = base64.b64encode(request.httprequest.files.get('professional_certifications').read()) if request.httprequest.files.get('professional_certifications') else False

        # training_certificates = base64.b64encode(request.httprequest.files.getlist('training_certificate').read()) if request.httprequest.files.get('training_certificate') else False
        training_ceritificates=request.httprequest.files.getlist('training_certificates')
        training_certificates_list=[]
        if 'training_certificates' in request.httprequest.files:
            training_certificates = request.httprequest.files.getlist('training_certificates')

            if training_certificates and any(training_certificates):
                for file in training_certificates:
                    file_data = base64.b64encode(file.read())
                    training_certificates_list.append({'file': file_data})

        #emergency contact
        contact_name=request.httprequest.form.getlist('contact_name')
        contact_phone=request.httprequest.form.getlist('contact_phone')
        relation=request.httprequest.form.getlist('relation')

        # bank info 
        bank_account_number=post.get('bank_account_number')
        bank_name=post.get('bank_name')
        account_name=post.get('account_name')

        if user:
            user.sudo().write({
                'user_name': user_name,
                'user_email': user_email if user_email else False,
                'age': age,
                'department': department,
                'temporary_address': temporary_address,
                'permanent_address': permanent_address,
                'phone': phone,
                'bank_account_number': bank_account_number,
                'bank_name': bank_name,
                'account_name': account_name,
                'position': position,
                'dob': post.get('dob') if post.get('dob') else False,  # Example for another field
                'nationality': post.get('nationality'),  # Example for another field
                'father_name': father_name,
                'mother_name': mother_name,
                'marital_status': marital_status,
                'partner_name': partner_name,
                'number_of_children': number_of_children,
                'grandfather_name': grandfather_name,
                'gender': gender,
                'passport_no': passport_no,
                'citizenship_no': citizenship_no,
                'issued_place': post.get('issued_place'),  # Example for another field
                'pan': pan,
                'related_skills': related_skills,
                'position': post.get('position'),  # Example for another field
            })
            if photo_encode:
                user.write({
                'photo': photo_encode,
                })
            if identification_file_encoded:
                user.write({
                    'identification_file': identification_file_encoded,
                })
            if cv_encoded:
                user.write({
                    'cv': cv_encoded,
                })
            if upload_pan_encoded:
                user.write({
                    'upload_pan': upload_pan_encoded,
                })
            if cover_letter:
                user.write({
                    'cover_letter': cover_letter,
                })
            if professional_certifications:
                user.write({
                    'professional_certifications': professional_certifications,
                })
            if training_certificates_list!=[]:
                user.sudo().write({
                'training_certificates': [(0, 0, {'name': f'File {i + 1}', 'datas': file_info['file']}) for i, file_info in enumerate(training_certificates_list)],
                })
        else:
            request.env['employee.registration.request'].sudo().create({
                'user_id': user_id,
                'user_name': user_name,
                'user_email': user_email if user_email else False,
                'age': age,
                'department': department,
                'temporary_address': temporary_address,
                'permanent_address': permanent_address,
                'phone': phone,
                'bank_account_number': bank_account_number,
                'bank_name': bank_name,
                'account_name': account_name,
                'position':position,
                'photo': photo_encode,
                'dob': post.get('dob') if post.get('dob') else False,  # Example for another field
                'nationality': post.get('nationality'),  # Example for another field
                'father_name': father_name,
                'mother_name': mother_name,
                'marital_status': marital_status,
                'partner_name': partner_name,
                'number_of_children': number_of_children,
                'grandfather_name': grandfather_name,
                'gender': gender,
                'passport_no': passport_no,
                'citizenship_no': citizenship_no,
                'issued_place': post.get('issued_place'),  # Example for another field
                'identification_file': identification_file_encoded,
                'pan': pan,
                'upload_pan': upload_pan_encoded,
                'related_skills': related_skills,
                'position': post.get('position'),  # Example for another field
                'cv': cv_encoded,
                'professional_certifications':professional_certifications,
                'cover_letter': cover_letter,
                'training_certificates': [(0, 0, {'name': f'File {i + 1}', 'datas': file_info['file']}) for i, file_info in enumerate(training_certificates_list)] or None,
                # 'status': 'pending',  # Example for another field
            })
        registration_request=request.env['employee.registration.request'].sudo().search([('user_id','=',request.env.user.id)])
        if(certificate_level[0]!=''):
            certificate_model = request.env['employee.education']
            for i in range(len(certificate_level)):
                certificate=certificate_model.sudo().search([('education_id','=',registration_request.id),('certificate_level','=',certificate_level[i]),('field_of_study','=',field_of_study[i])])
                if(certificate):
                    certificate.write({
                        'education_id': registration_request.id,
                        'graduation_year': graduation_year[i],
                        'institution_name': institution_name[i],
                        'certificate_level': certificate_level[i],
                        'field_of_study': field_of_study[i],
                    })
                else:
                    certificate=certificate_model.create({
                        'education_id':registration_request.id,
                        'graduation_year':graduation_year[i]or None,
                        'institution_name': institution_name[i],
                        'certificate_level': certificate_level[i],
                        'field_of_study': field_of_study[i],
                        # 'academic_certificates': [(0, 0, {'name': f'File {j + 1}', 'datas': file_info['file']}) for j, file_info in enumerate(academic_certificates[i])] or None,
                    })
                if 0 <= i < len(academic_certificates):
                    academic_files = []
                    for j, file_info in enumerate(academic_certificates[i]):
                        f_content = file_info['file']
                        academic_files.append((0, 0, {'name': f'File {j + 1}', 'datas': f_content}))

                    certificate.sudo().write({
                        'academic_certificates': academic_files,
                    })
        if(worked_position[0]!=''):
            for i in range(len(worked_position)):
                worked=request.env['employee.work.experience'].search([('request_id','=',registration_request.id),('job_position','=',worked_position[i]),('company_name','=',company_name[i])])
                if(worked):
                    worked.write({
                        'request_id': registration_request.id,
                        'job_position': worked_position[i],
                        'duration_of_employment': duration_of_employment[i],
                        'company_name': company_name[i],
                        'exit_reason': exit_reason[i],
                    })
                else:
                    request.env['employee.work.experience'].create({
                        'request_id':registration_request.id,
                        'job_position':worked_position[i],
                        'duration_of_employment':duration_of_employment[i],
                        'company_name':company_name[i],
                        'exit_reason':exit_reason[i],
                    })
        if(contact_phone[0]!=''):
            for i in range(len(contact_phone)):
                contact=request.env['employee.emergency.contact'].search([('emergency_id','=',registration_request.id),('contact_phone','=',contact_phone[i])])
                if contact:
                    contact.write({
                        'emergency_id': registration_request.id,
                        'contact_name': contact_name[i],
                        'contact_phone': contact_phone[i],
                        'relation': relation[i],
                    })
                else:
                    request.env['employee.emergency.contact'].create({
                        'emergency_id':registration_request.id,
                        'contact_name':contact_name[i],
                        'contact_phone':contact_phone[i],
                        'relation':relation[i],
                    })
        return request.redirect("/")