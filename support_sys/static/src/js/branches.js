odoo.define('employee_dashboard.view_branches', function (require) {
    "use strict";
var publicWidget=require("web.public.widget");
var core=require("web.core");

publicWidget.registry.ViewBranches = publicWidget.Widget.extend({
     selector: '.daily_tasks',
     events: {
            'change select#client':"_showBranch",
        },
        _showBranch:function(evt){
            var client = document.getElementById('client').value;
            console.log(client)
            client=parseInt(client)
            var branches = $(evt.currentTarget).data('branches');
            var filtered=null
            console.log(branches)
            if(branches!==''){
              filtered= branches.filter((data)=>{
                return data.client===client
                })
            }
            console.log(filtered)
            if(filtered && filtered.length>0){
             var branchesSelect = document.getElementById('branch');
                var branch_showing=document.querySelector('.branch_showing')
                branch_showing.style.display='flex'
        // Clear existing options
        branchesSelect.innerHTML = '';

        // Add new options based on filtered branches
        filtered.forEach((branch) => {
            var option = document.createElement('option');
            option.value = branch.id; // Set the value attribute based on your data
            option.textContent = branch.name; // Set the text content based on your data
            branchesSelect.appendChild(option);
            })
            }
            else{
             var branch_showing=document.querySelector('.branch_showing')
                branch_showing.style.display='none'
            }
        },
    });

});