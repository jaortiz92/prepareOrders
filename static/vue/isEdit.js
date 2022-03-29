const isEdit = {
    compilerOptions: {
        delimiters: ['[[', ']]']
        
      },
    data() {
        return {
            show: false
        }
    },
    mounted() {
        if(localStorage.getItem('show') === 'true') {this.show = true}
        else {this.show = false};
    },
    methods:{
        showButton: function (){
            if (this.show){this.show = false;} 
            else {this.show = true;}
            localStorage.setItem('show', this.show);
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
        },

        deleteProductOrder: function(id){
            Swal.fire({
                "title": "¿Estas seguro?",
                "text": `Se eliminará la Producto ${id}`,
                "icon": "question",
                "showCancelButton": true,
                "cancelButtonText": "No, Cancelar",
                "confirmButtonText": "Si, Eliminar",
                "confirmButtonColor": "#c82333"
            })
                .then((result) => {
                    if (result.isConfirmed) {
                        window.location.href = "/orders/products/delete_product_order/" + id
                    }
                })
        }

    }

    
}

Vue.createApp(isEdit).mount('#is-edit')
