odoo.define('employee_dashboard.leave_request',function(require){
    "use strict";
    var rpc = require("web.rpc");
    var publicWidget = require('web.public.widget');
    const Dialog = require('web.Dialog');
    

    publicWidget.registry.LeaveRequest = publicWidget.Widget.extend({
        selector: '.oe_leave_request_submit',
        init: function(parent,context){
            this._super(parent,context);
        },
        start: function(){
            this.showDialog()
        },
        showDialog: function(){
            console.log("Hello Damodar from js")
            // Dialog.alert(this,"Submission Successful Man")
        }
    })
})

odoo.define('employee_dashboard.attendance_check', function (require) {
    "use strict";

    var publicWidget = require('web.public.widget');
    var Dialog = require('web.Dialog');

    publicWidget.registry.AttendanceCheck = publicWidget.Widget.extend({
        selector: '.attendance-container',
        events: {
            'click .check-button': '_onCheckButtonClick',
        },

        start: function () {
            this._super.apply(this, arguments);
            this.$checkButton = this.$('.check-button');
            this.$proofFile=this.$('#cameraInput');
            this.$validationMessage=this.$('#validationMessage')
            this.$checkInTime = this.$('.check-in-time');
            this.$checkOutTime = this.$('.check-out-time');
            this.isCheckIn = true;
            this.checkInFormattedTime = null;
            this.checkOutFormattedTime = null;
            var state=localStorage.getItem('state')
            var last_check_in_date=localStorage.getItem('check_in_date');
            var currentTime=new Date()
            var year = currentTime.getFullYear();
            var month = (currentTime.getMonth() + 1).toString().padStart(2, '0'); // Note: Months are zero-based, so we add 1
            var day = currentTime.getDate().toString().padStart(2, '0');
            var date= year + '-' + month + '-' + day;
            if(last_check_in_date<date){
                localStorage.setItem('state','good-bye')
            }

            if(state==='check-in'){
            this.$checkButton.removeClass('check-in').addClass('ok-class');
              this.$checkButton.text('OK');
                this.$checkButton.css({
                    'background-color':'#71639e',
                    'color':'white'
                });
                var check_in_time=localStorage.getItem('check_in_time')
                this.$checkInTime.text('Checked In at '+ check_in_time)
                this.$checkInTime.css('display','block')
                this.$proofFile.css('display','none')
            }
            else if(state==='ok-class'){
            console.log('state is ok-class so class must be check-out')
                this.$checkInTime.css('display','none')
              this.$checkButton.removeClass('check-in').addClass('check-out');
                 this.$checkButton.text('Check Out');
                this.$checkButton.css({
                    'background-color':'red',
                    'color':'white'
                });
                this.$checkInTime.css('display','none')
            }
             else if(state==='check-out'){
            this.$checkButton.removeClass('check-in').addClass('good-bye');
                this.$checkButton.css({
                    'background-color':'yellow',
                    'color':'black'
                });
                this.$checkButton.text('Good Bye!!')
                var check_out_time=localStorage.getItem('check_out_time')
                this.$checkOutTime.text('Checked Out at '+ check_out_time)
                this.$checkOutTime.css('display','block')
                this.$proofFile.css('display','none')
            }
            else if(state==='good-bye'){
                this.$checkOutTime.css('display','none')
            }

        },

        _onCheckButtonClick: function (evt) {
        var user=$(evt.currentTarget).data('user');
            if (this.$checkButton.hasClass('check-in')) {
                if(!this.$proofFile[0].files.length){
                this.$validationMessage.text('Please capture a image for proof')
                this.$validationMessage.css('display','block')
                }
                else{
                var image=this.$proofFile[0].files[0]
                console.log(image)
                this.$validationMessage.css('display','none')
                var punch_type='0'
                var currentTime = new Date()
                var year = currentTime.getFullYear();
                var month = (currentTime.getMonth() + 1).toString().padStart(2, '0'); // Note: Months are zero-based, so we add 1
                var day = currentTime.getDate().toString().padStart(2, '0');
                var date= year + '-' + month + '-' + day;
                var hours = currentTime.getHours().toString().padStart(2, '0');
                var minutes = currentTime.getMinutes().toString().padStart(2, '0');
                var seconds = currentTime.getSeconds().toString().padStart(2, '0');
                this.checkInFormattedTime = hours + ':' + minutes + ':' + seconds;
                localStorage.setItem('check_in_date',date)
                localStorage.setItem('check_in_time',this.checkInFormattedTime)
                this._saveDataInAllLog(user,punch_type,this.checkInFormattedTime,image)
                localStorage.setItem('state','check-in')
                 this.$checkButton.removeClass('check-in').addClass('ok-class');
                this.$checkButton.text('OK');
                this.$checkButton.css({
                    'background-color':'#71639e',
                    'color':'white'})
                    this.$checkInTime.text('Checked In at '+ this.checkInFormattedTime)
                this.$checkInTime.css('display','block')
                this.$proofFile.css('display','none')
                }
            }
            else if(this.$checkButton.hasClass('ok-class')){
                localStorage.setItem('state','ok-class')

                this.$checkButton.removeClass('ok-class').addClass('check-out');
                this.$checkButton.text('Check Out');
                this.$checkButton.css({
                    'background-color':'red',
                    'color':'white'
                });
                this.$checkInTime.css('display','none')
                 this.$proofFile.val('');
                this.$proofFile.trigger('change');
                this.$proofFile.css('display','block')
            }
            else if(this.$checkButton.hasClass('check-out')){
                if(!this.$proofFile[0].files.length){
                this.$validationMessage.text('Please capture a image for proof')
                this.$validationMessage.css('display','block')
                }
                else{
                var image=this.$proofFile[0].files[0]
                console.log(image)
                this.$validationMessage.css('display','none')
                var currentTime = new Date()
                var year = currentTime.getFullYear();
                var month = (currentTime.getMonth() + 1).toString().padStart(2, '0'); // Note: Months are zero-based, so we add 1
                var day = currentTime.getDate().toString().padStart(2, '0');
                var date= year + '-' + month + '-' + day;
                localStorage.setItem('state','check-out')
                var punch_type='1'
                var hours = currentTime.getHours().toString().padStart(2, '0');
                var minutes = currentTime.getMinutes().toString().padStart(2, '0');
                var seconds = currentTime.getSeconds().toString().padStart(2, '0');
                this.checkOutFormattedTime = hours + ':' + minutes + ':' + seconds;
                localStorage.setItem('check_out_date',date)
                localStorage.setItem('check_out_time',this.checkOutFormattedTime)
                var check_in_time_from_storage=localStorage.getItem('check_in_time')
                this._saveDataInAllLog(user,punch_type,this.checkOutFormattedTime,image)
                  this.$checkButton.removeClass('check-out').addClass('good-bye');
                this.$checkButton.css({
                    'background-color':'yellow',
                    'color':'black'
                });
                this.$checkButton.text('Good Bye!!')
                this.$checkOutTime.text('Checked Out at '+ this.checkOutFormattedTime)
                this.$checkOutTime.css('display','block')
                this.$proofFile.css('display','none')
                }
            }
            else if(this.$checkButton.hasClass('good-bye')){
                localStorage.setItem('state','good-bye')

                this.$checkButton.removeClass('good-bye').addClass('check-in');
                this.$checkButton.text('Check In')
                this.$checkButton.css({
                    'background-color':'green',
                    'color':'white'
                });
                this.$checkInTime.css('display','none')
                this.$checkOutTime.css('display','none')
                this.$proofFile.val('');
                this.$proofFile.trigger('change');
                this.$proofFile.css('display','block')
            }
            else{
                return null;
            }
        },
        async _saveDataInAllLog (user,punch_type,checkIn,image){
        var self=this;
        var location= await self._compute_location()
       var currentAddress=await self._get_address(location.latitude,location.longitude)
        console.log(currentAddress)
        var get_check_in_date=localStorage.getItem('check_in_date')
        var checkInTimestamp=get_check_in_date + ' ' + checkIn
        console.log(checkInTimestamp)
         const nepaliDate = new Date(checkInTimestamp);

    // Convert to UTC string
        const utcTimestamp = nepaliDate.toISOString();
        console.log(utcTimestamp)
   const utcMoment = moment.utc(utcTimestamp);

    // Format the date to 'YYYY-MM-DD HH:mm:ss' in UTC
    const UTCFormattedTimestamp = utcMoment.format('YYYY-MM-DD HH:mm:ss');

      var reader = new FileReader();
    reader.readAsDataURL(image);
    reader.onloadend = function () {
        var base64Image = reader.result.split(',')[1];

        // Send data to the backend with the image as a base64-encoded string
        self._rpc({
            model: 'all.log.attendance',
            method: 'create',
            args: [{
                'employee': user,
                'punch_type': punch_type,
                'punching_time': UTCFormattedTimestamp,
                'punching_latitude': location.latitude,
                'punching_longitude': location.longitude,
                'punching_address': currentAddress,
                'proof': base64Image,
            }],
        }).then(function (result) {
            console.log("Successfully added");

        }).guardedCatch(function (error) {
            console.error("Error while saving data:", error);
        });
    };
        },
        async _compute_location(){
        var currentLocation=null;
//        console.log("location computing")
        return new Promise((resolve, reject) => {
         if ("geolocation" in navigator) {
    // Get the current location
    navigator.geolocation.getCurrentPosition(
        function(position) {
            var latitude = position.coords.latitude;
            var longitude = position.coords.longitude;
            currentLocation= {latitude,longitude}
            // Do something with the latitude and longitude
            console.log("Latitude:", latitude);
            console.log("Longitude:", longitude);
            resolve(currentLocation)
        },
        function(error) {
            // Handle errors
            console.error("Error getting location:", error.message);
            reject(error)
        }
    );
} else {
    // Geolocation is not supported
    console.error("Geolocation is not supported by this browser.");
    reject(new Error("Geolocation is not supported"));
}
})
        },
   async _get_address(latitude,longitude){
        var self = this;
        return new Promise((resolve, reject) => {
        $.ajax({
        url: `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            var address = data.display_name.match(/^(.*?),/);
            var inputValue = address.input.split(',').slice(0, 3).join(',');
            var city=data.address.city || data.address.town || data.address.village;
//            var street=data.address.road || data.address.pedestrian || data.address.suburb;;
//            var country=data.address.country;
//            var zip=data.address.postcode;
            var fullAddress=inputValue + ', '+ city
            resolve(fullAddress)
        },
        error: function (error) {
            console.error('Error fetching address:', error);
        reject(error)
        }
    });
    })

   },
    });

});

odoo.define("employee_dashboard.yearly_calendar_integration",function(require){
'use strict';

var calendarIntegrationInitializations=require('employee_dashboard.calender_initializations')
var publicWidget=require("web.public.widget");
 var rpc = require('web.rpc');
var core=require("web.core");

publicWidget.registry.CalendarIntegration=publicWidget.Widget.extend({
    selector:'#calendar_integration',
    events:{

        'click button#yearView':"_yearView",
        'click button#monthView':"_monthView",
        'click button#weekView':"_weekView",

    },
    state:{

    event:[]
    },
   async start(){
    await this._getAllEvents()
    calendarIntegrationInitializations.initializeFullCalendarMonth('calendar','dayGridMonth',this.state.event)
    },
    _yearView(evt){
    document.querySelector('#calendar').innerHTML=''
    calendarIntegrationInitializations.initializeFullCalendarYear('#calendar',this.state.event)
    },
    _monthView(evt){
       document.querySelector('#calendar').innerHTML=''
    calendarIntegrationInitializations.initializeFullCalendarMonth('calendar','dayGridMonth',this.state.event)
    },
       _weekView(evt){
       document.querySelector('#calendar').innerHTML=''
    calendarIntegrationInitializations.initializeFullCalendarMonth('calendar','dayGridWeek',this.state.event)
    },
   async _getAllEvents(){
    var self=this
       await rpc.query({
        model:'office.calender',
        method:'search_read',
        args:[],
        kwargs:{fields:{}},
        }).then(function(result){
            console.log(result);
            self.state.event=result
//            console.log('logged from get',self.state.event)
        })
    },
})

})

odoo.define('employee_dashboard.calender_initializations', function (require) {
    'use strict';

    var calendar=null;

    var initializeFullCalendarMonth = function (id,format,events) {
            var event=[];
            if(events){
             event = events.map(function (obj) {
            return { title: obj.display_name, start: obj.holiday_date,end:obj.holiday_date};
            });
            }

            var fullCalendarCSS = document.createElement('link');
            fullCalendarCSS.rel = 'stylesheet';
            fullCalendarCSS.href = 'https://cdn.jsdelivr.net/npm/fullcalendar@5.10.1/main.css';
            document.head.appendChild(fullCalendarCSS);

            var fullCalendarJS = document.createElement('script');
            fullCalendarJS.src = 'https://cdn.jsdelivr.net/npm/fullcalendar@5.10.1/main.js';
            fullCalendarJS.async = true;
            fullCalendarJS.onload = function(){
               var calendarEl = document.getElementById(id)
;
         calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: `${format}`,
            headerToolbar: {
                left: 'prev today next',
                center: 'title',
                  right:'',
            },
            editable:true,
            events: event,
        });

        calendar.render();
            }
            document.head.appendChild(fullCalendarJS);

    };

  var initializeFullCalendarYear = function (id,events) {
            var event=[];
            var filtered=events.filter(function(obj){
            return obj.holiday_date&&obj.holiday_date!==false
            })
            console.log(filtered)
            if(filtered){
            console.log("found holidays")
             event = filtered.map(function (obj) {
             if(obj.holiday_date!==false){
             console.log("inside")
             var dateComponents=obj.holiday_date.split("-");
             var jsDate=new Date(parseInt(dateComponents[0]), parseInt(dateComponents[1]) - 1, parseInt(dateComponents[2]))
             var dateComponents1=obj.holiday_date.split("-");
             var jsDate1=new Date(parseInt(dateComponents1[0]), parseInt(dateComponents1[1]) - 1, parseInt(dateComponents1[2]))
            return { name: obj.display_name, startDate: jsDate,endDate:jsDate1 };
             }
            });
            }
//            if(calendar){
//              calendar.destroy()
//              calendar=null;
//            }
            var fullCalendarYearCSS = document.createElement('link');
            fullCalendarYearCSS.rel = 'stylesheet';
            fullCalendarYearCSS.href = 'https://unpkg.com/js-year-calendar@latest/dist/js-year-calendar.min.css';
            document.head.appendChild(fullCalendarYearCSS);

            var fullCalendarYearJS = document.createElement('script');
            fullCalendarYearJS.src = 'https://unpkg.com/js-year-calendar@latest/dist/js-year-calendar.min.js';
            fullCalendarYearJS.async = true;
            fullCalendarYearJS.onload = function(){
              calendar= new Calendar(document.querySelector(id),{
            enableContextMenu: true,
            enableRangeSelection: true

        });
               calendar.setDataSource(event)


            }
            document.head.appendChild(fullCalendarYearJS);
    };

    return {
        initializeFullCalendarMonth:initializeFullCalendarMonth,
        initializeFullCalendarYear: initializeFullCalendarYear,
    };
});