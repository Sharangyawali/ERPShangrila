odoo.define('employee_dashboard.view_profile', function (require) {
    "use strict";

    var publicWidget = require('web.public.widget');
    var Dialog = require('web.Dialog');

    publicWidget.registry.ProfileView = publicWidget.Widget.extend({
        selector: '.profile_container',
        events: {
            'change input#editImageInput':"_imageInput",
            'click .profile-button': '_onProfileButtonClick',
        },

        start: function () {
        this.$profileButton = this.$('.profile-button');
        this.$profile=this.$('.edit-icon')
        this.$street = this.$('.street');
        this.$city = this.$('.city');
        this.$zip = this.$('.zip');
        this.$email = this.$('.email');
        this.$mobile = this.$('.mobile');
        this.$phone = this.$('.phone');
        this.$birthdate = this.$('.birthdate');
        this.$marital_status = this.$('#marital_status');
        this.$degree_of_study = this.$('#degree_of_study');
        this.$study_field = this.$('.study_field');
        this.$study_school = this.$('.study_school');
        this.$bank_detail = this.$('.bank_detail');
        this.$passport_no = this.$('.passport_no');
        },
        _imageInput:function(evt){
            var image=$(evt.currentTarget)
            if(image[0].files){
            console.log(image[0].files[0])
            var reader=new FileReader();
            reader.onload=function(e){
            document.querySelector('.image_tag').src=e.target.result
            }
            reader.readAsDataURL(image[0].files[0])
            }
        },
       _onProfileButtonClick: function (evt) {
        if (!this.$profileButton.data('clicked')) {

               this.$street.removeAttr('readonly')
               $('.edit-icon').css('display','block')
               this.$city.removeAttr('readonly')
               this.$zip.removeAttr('readonly')
               this.$email.removeAttr('readonly')
               this.$mobile.removeAttr('readonly')
               this.$phone.removeAttr('readonly')
               this.$marital_status.removeAttr('disabled')
               this.$degree_of_study.removeAttr('disabled')
               this.$study_field.removeAttr('readonly')
               this.$study_school.removeAttr('readonly')
               this.$bank_detail.removeAttr('readonly')
               this.$passport_no.removeAttr('readonly')
                this.$profileButton.text('Save Profile')
                this.$profileButton.data('clicked', true);
                 evt.preventDefault();
        }
        else{
            this.$profileButton.removeData('clicked');
        }
    },

    });

});