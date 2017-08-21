{% load instant_tags i18n %}
var allApps = [];
{% for app, models in appmodels.items %}
	allApps["{{app}}"] = [];
	allModels = [];
	{% for model in models %}
		allModels.push("{{model}}");
	{% endfor %}
	allApps.push({"appname": "{{app}}", "models": allModels});
{% endfor %}

const app = new Vue({
	el: '#app',
	delimiters: ["${", "}"],
	mixins: [vvMixin],
    data () {
        return {
        	apps: allApps  	
        }
	},
	methods: {
		allModels: function(){
			console.log("all")
		},
	},
});