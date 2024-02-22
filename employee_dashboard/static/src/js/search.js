odoo.define('employee_dashboard.search_view', function (require) {
    "use strict";
console.log("is reading")
var publicWidget=require("web.public.widget");
var core=require("web.core");

publicWidget.registry.SearchView = publicWidget.Widget.extend({
     selector: '.department_details',
     events: {
            'click button#search':"_searchInput",
        },
        _searchInput:function(evt){
            var searchData = document.getElementById('searchValue').value;
            var attendance = $(evt.currentTarget).data('attendance');
            if(searchData!==''){
            var filtered=attendance.filter((att)=>{
            const searchValue=searchData.toLowerCase()
            const name=att.name.toLowerCase();
               return searchValue&&name.includes(searchValue)
            })
            console.log(filtered)
            this._updateTable(filtered)
            }
            else{
            this._updateTable(attendance)
            }

        },
       _updateTable:function(attendance){
       $('.department_details tbody tr').remove();
        attendance.map((att)=>{
        const options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit',hour12: false, };
        var formattedCheckIn=new Intl.DateTimeFormat('en-US',options).format(new Date(att.check_in));
        var formattedCheckOut=new Intl.DateTimeFormat('en-US',options).format(new Date(att.check_out));
        var checkin_add=att.checkin_add
        if(checkin_add===false){
        checkin_add=''
        }
        var checkout_add=att.checkout_add
        if(checkout_add===false){
        checkout_add=''
        }
         var newRow = `<tr>
                    <th scope="row"><span id="id">${att.id}</span></th>
                    <td><span id="name">${att.name}</span></td>
                    <td><span id="check_in">${formattedCheckIn}</span></td>
                    <td><span id="checkin_add">${checkin_add}</span></td>
                    <td><span id="check_out">${formattedCheckOut}</span></td>
                    <td><span id="checkout_add">${checkout_add}</span></td>
                    <td><span id="worked_hours">${att.worked_hour}</span></td>
                </tr>`;
                $('.department_details tbody').append(newRow);
        })
       },
    });

});