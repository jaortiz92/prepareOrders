const isEdit = {
    compilerOptions: {
        delimiters: ['${', '}']
        
      },
    data() {
        return {
            prueba : 'Hello world',
            show: false
        }
    },
    methods:{
        showButton: function (){
            if (this.show){
                this.show = false    
            } else {
                this.show = true
            }
        },

        deleteOrder: function(id, value){
            Swal.fire({
                "title": "¿Estas seguro?",
                "text": `Se eliminará la orden ${id} del archivo ${value}`,
                "icon": "question",
                "showCancelButton": true,
                "cancelButtonText": "No, Cancelar",
                "confirmButtonText": "Si, Eliminar",
                "confirmButtonColor": "#c82333"
            })
                .then((result) => {
                    if (result.isConfirmed) {
                        window.location.href = "delete_order/" + id
                    }
                })
        }

    }

    
}

Vue.createApp(isEdit).mount('#is-edit')
