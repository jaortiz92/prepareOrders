const changeTotals = {
    compilerOptions: {
        delimiters: ['[[', ']]']
        
      },
    data() {
        return {
        }
    },
    mounted(){
    },
    methods:{
        onChange: function (){
            let cost = document.getElementById("id_cost").value
            let price = document.getElementById("id_price").value
            let quantity = document.getElementById("id_quantity").value
            document.getElementById("id_total_cost").value = cost * quantity;
            document.getElementById("id_total_price").value = price * quantity;
       }
    }
}

Vue.createApp(changeTotals).mount('#change-totals')
