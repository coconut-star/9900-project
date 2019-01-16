<template>
<div class="card card-small">
    <div class="card-header user-header alt bg-dark">
        <div class="media">
            <a href="#" @click="view_details">
                <img class="align-self-center rounded-circle mr-3" style="width:85px; height:85px;" alt="" v-if="real_avatar_path" :src="real_avatar_path">
                <img class="align-self-center rounded-circle mr-3" style="width:85px; height:85px;" alt="" v-else src="../assets/images/default.png">
            </a>
            <div class="media-body">
                <h2 class="text-light display-6">{{match.job.name}}</h2>
                <p>
                    {{match.job.contact_person.company}}<br>
                    {{match.job.contact_person.website}}
                </p>
            </div>
        </div>
    </div>

    <table>
        <tr><td colspan="2"><i class="fa fa-tasks"></i> {{match.job.description}}</td></tr>
        <tr>
            <td><i class="fa fa-map-marker"></i> {{match.job.city}}</td>
            <td><i class="fa fa-money"></i> {{salary}}</td>
        </tr>
        <tr>
            <td><i class="fa fa-bell-o"></i> {{match.job.contact_person.user.phone}}</td>
            <td><i class="fa fa-calendar"></i> {{match.job.date_posted}}</td>
        </tr>
        <tr>
            <td colspan="2"><i class="fa fa-envelope-o"></i> {{match.job.contact_person.user.email}}</td>
        </tr>
    </table>
    <div class="match-controls">
        <div class="match-status">
            <h3>{{state_name}}</h3>
        </div>
        <button v-if="can_express_interest" type="button" class="btn" @click='express_interest()'>Express Interest</button>
        <button v-if="can_decline" type="button" class="btn" @click='decline_match()'>Decline</button>
        <button v-if="job_offer_available" type="button" class="btn" @click='accept_job_offer()'>Accept Job Offer</button>
        <button v-if="job_offer_available" type="button" class="btn" @click='decline_job_offer()'>Decline Job Offer</button>
        <!-- Render this dummy button if no other buttons are visible. This is a hack to keep the card height the same. -->
        <button v-if="no_action_possible" type="button" class="btn ghost">X</button>
    </div>
</div>
</template>

<script>
import axios from 'axios'
import * as ss from '../assets/js/skillstash.js';
export default {
    name: 'JobCard',
    props: ['match'],
    data() {
        return {

        }
    },
    computed: {
        can_express_interest() {
            let state = this.match.state;
            // Candidates are allowed to change their minds about declining jobs,
            // although the employers may no longer be interested.
            return state == 'N' || state == 'EI' || state == 'DC' || this.match.state == 'JD';
        },
        can_decline() {
            let state = this.match.state;
            return state == 'N' || state == 'CI' || state == 'EI' || state == 'P';
        },
        job_offer_available() {
            return this.match.state == 'JO';
        },
        no_action_possible() {
            let state = this.match.state;
            return state == 'DE' || state == 'H' || state == 'F' || state == 'W';
        },
        real_avatar_path() {
            let person = this.match.job.contact_person;
            if (person.photo == '')
                return null;
            return API_HOST + '/api/download/' + person.user.id +  '/' + person.photo;
        },
        salary() {
            let pay_type = this.match.job.pay_type;
            let pay_period = '';
            if (pay_type === 'D')
                pay_period = 'Day';
            else if (pay_type === 'H')
                pay_period = 'Hour';
            else if (pay_type === 'M')
                pay_period = 'Month';
            else if (pay_type === 'Y')
                pay_period = 'Year';
            return '$' + this.match.job.pay + ' / ' + pay_period;
        },
        state_name() {
            return ss.match_state_names[this.match.state];
        }
    },
    methods: {
        express_interest() {
            axios({
                method: 'post',
                url: API_HOST + '/api/job-matches/' + this.match.id + '/express_interest/'
            }).then((response) => {
                if (response.status === 200 || response.status === 201) {
                    this.match.state = response.data.state;
                }
            }).catch(function (error) {
                alert(error.response.data)
            })
        },
        decline_match() {
            axios({
                method: 'post',
                url: API_HOST + '/api/job-matches/' + this.match.id + '/decline/'
            }).then((response) => {
                if (response.status === 200 || response.status === 201) {
                    this.match.state = response.data.state;
                }
            }).catch(function (error) {
                alert(error.response.data)
            })
        },
        accept_job_offer() {
            if (!confirm("Are you sure that you want to decline the offer of the job " + this.match.job.name
                 + "? This action cannot be undone."))
                return;
            axios({
                method: 'post',
                url: API_HOST + '/api/job-matches/' + this.match.id + '/accept_job_offer/'
            }).then((response) => {
                if (response.status === 200 || response.status === 201) {
                    this.match.state = response.data.state;
                }
            }).catch(function (error) {
                alert(error.response.data)
            })
        },
        decline_job_offer() {
            if (!confirm("Are you sure that you want to decline the offer of the job " + this.match.job.name + "?"))
                return;
            axios({
                method: 'post',
                url: API_HOST + '/api/job-matches/' + this.match.id + '/decline_job_offer/'
            }).then((response) => {
                if (response.status === 200 || response.status === 201) {
                    this.match.state = response.data.state;
                }
            }).catch(function (error) {
                alert(error.response.data)
            })
        },
        view_details() {
            this.$emit('job_clicked', this.match.job);
        }
    }
}
</script>

<style lang="scss">
@import '../assets/css/skillstash.css';


.mr-3,
.mx-3 {
    margin-right: 1rem !important;
}

h1,
h2,
h3,
h4,
h5,
h6 {
    margin: 0 !important;
}

.text-light {
    color: #f8f9fa !important;
}

.badge-primary {
    color: #fff !important;
    background-color: #007bff !important;
}

.badge-danger {
    color: #fff !important;
    background-color: #dc3545 !important;
}

.badge-success {
    color: #fff !important;
    background-color: #28a745 !important;
}

.badge-warning {
    color: #212529 !important;
    background-color: #ffc107 !important;
}

.badge {
    display: inline-block !important;
    padding: .25em .4em !important;
    font-size: 75% !important;
    font-weight: 700 !important;
    line-height: 1 !important;
    text-align: center !important;
    white-space: nowrap !important;
    vertical-align: baseline !important;
    border-radius: .25rem !important;
}

a,
button {
    text-decoration: none !important;
    outline: none !important;
    color: #878787 !important;
    -webkit-transition: all 0.25s ease !important;
    transition: all 0.25s ease;
}
</style>

<style>
@import 'font-awesome/css/font-awesome.min.css';
@import '../../static/assets/css/build.css';
@import '../../static/assets/css/normalize.css';
@import '../../static/assets/css/themify-icons.css';
@import '../../static/assets/css/cs-skin-elastic.css';
</style>
