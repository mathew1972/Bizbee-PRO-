
frappe.ui.form.on('Quotation-', {
    refresh: function (frm){
        frm.add_custom_button (__( 'Employee'), function() {
            frm.call({
                doc:frm.doc,
                method: 'get_employee',
                
            }).then(r =>{
                var data=r.message
                console.log(data)
                let d = new frappe.ui.Dialog({
                    title: 'Employee Details',
                    size: 'extra-large',
                    fields:[    
                        {
                            label: 'Employee Data',
                            fieldname: 'data',
                            fieldtype: 'Table',
                            options: 'Employee Ckeck',
                            data:data,
                            fields:[
                                {
                                    label: 'Employee',
                                    fieldname: 'employee',
                                    fieldtype: 'Data', in_list_view:1,
                                    in_list_view:1,                                                                
                                },
                            ]
                       }
                    ],
                    primary_action_label: 'Get Items',
                    primary_action(values){
                        let selectedItem=cur_dialog.fields_dict.data.grid.get_selected_children();
                        frm.call({
                            doc:frm.doc,
                            method:'add_employee',
                            args:{
                               selections: selectedItem                               
                            }
                        }) 
                        d.hide();                    
                    }

                });
                d.show();
            });

        },__('Get Employee'));        
    }

});