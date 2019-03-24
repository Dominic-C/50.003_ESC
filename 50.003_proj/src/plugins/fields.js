export default {
    props: {
        item : {
            type: Object,
            required: true
        },
        error: {
            required: true
        }
    },
    methods: {
        updateValue(e){
            this.$emit('input', e.target.value)
        }
    },
    created (){
        this.item.value && (this.$parent.value = this.item.value)
    }
}