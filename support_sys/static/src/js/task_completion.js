odoo.define("support_sys.task_completed",function(require){
'use strict';

var publicWidget=require("web.public.widget");
var core=require("web.core");

var _t=core._t;

publicWidget.registry.TaskCompleted=publicWidget.Widget.extend({
    selector:'#table_assigned_task',
    events:{
        'click button#task_completed':"_taskCompleted",
    },
    _taskCompleted:function(evt){
    var self=this;
    var taskId=$(evt.currentTarget).data('id');
    console.log("completed clicked:",taskId)
    var date=new Date()
    this._rpc({
        model:'employee.task.assignment',
        method:'write',
        args:[[taskId],{status:'completed',completed_date:date}]
    }).then((result)=>{
    if(result){
    console.log("Task complete of Id",taskId)
    location.reload()
    }
    else{
    console.log("Failed to mark")
    }
    })
    },

})

})
odoo.define("support_sys.task_not_completed",function(require){
'use strict';

var publicWidget=require("web.public.widget");
var core=require("web.core");

var _t=core._t;

publicWidget.registry.TaskNotCompleted=publicWidget.Widget.extend({
    selector:'#table_completed_task',
    events:{
        'click button#task_not_completed':"_taskNotCompleted",
    },
    _taskNotCompleted:function(evt){
    var self=this;
    var taskId=$(evt.currentTarget).data('id');
    console.log("completed clicked:",taskId)
    this._rpc({
        model:'employee.task.assignment',
        method:'write',
        args:[[taskId],{status:'onprogress',completed_date: null}]
    }).then((result)=>{
    if(result){
    console.log("Task not completed of Id",taskId)
    location.reload()
    }
    else{
    console.log("Failed to mark")
    }
    })
    },

})

})