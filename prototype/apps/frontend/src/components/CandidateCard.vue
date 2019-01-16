<!-- CandidateCard -->
<!-- * Displays candidate information. -->
<!-- * Used in Employer, Recruiter profiles, and on the JobMatch page.-->
<template>
<div class="card card-small">
    <div class="card-header user-header alt bg-dark">
        <div class="media">
            <a href="#" @click="view_details">
                <img class="align-self-center rounded-circle mr-3" style="width:85px; height:85px;" alt="" v-if="real_avatar_path" :src="real_avatar_path">
                <img class="align-self-center rounded-circle mr-3" style="width:85px; height:85px;" alt="" v-else src="../assets/images/default.png">
            </a>
            <div class="media-body">
                <h2 class="text-light display-6">{{match.candidate.user.first_name}} {{match.candidate.user.last_name}}</h2>
                <p>
                    {{match.job.name}}<br>
                    Suitability Score {{match.score}}
                </p>
            </div>
        </div>
    </div>
    <ul class="list-group list-group-flush">
        <li><i class="fa fa-map-marker"></i> {{match.candidate.user.city}}</li>
        <li><i class="fa fa-graduation-cap"></i> {{education_name}}</li>
        <li><i class="fa fa-bell-o"></i> {{match.candidate.user.phone}}</li>
        <li><i class="fa fa-envelope-o"></i> {{match.candidate.user.email}}</li>
    </ul>
    <div class="match-controls">
        <div class="match-status">
            <h3>{{state_name}}</h3>
        </div>
        <button v-if="!no_buttons && can_express_interest" type="button" class="btn" @click='express_interest()'>Express Interest</button>
        <button v-if="!no_buttons && can_decline" type="button" class="btn" @click='decline_match()'>Decline</button>
        <button v-if="!no_buttons && can_make_job_offer" type="button" class="btn" @click='make_job_offer()'>Make Job Offer</button>
        <button v-if="!no_buttons && can_withdraw_job_offer" type="button" class="btn" @click='withdraw_job_offer()'>Withdraw Job Offer</button>
        <!-- Render this dummy button if no other buttons are visible. This is a hack to keep the card height the same. -->
        <button v-if="no_buttons || no_action_possible" type="button" class="btn ghost">X</button>
    </div>
</div>
</template>

<!-- JavaScript -->
<script>
import axios from 'axios'
import * as ss from '../assets/js/skillstash.js';
export default {
    name: 'CandidateCard',
    props: ['match', 'no_buttons'],
    data() {
        return {

        }
    },
    computed: {
        can_express_interest() {
            let state = this.match.state;
            // Employers are allowed to change their minds about declining candidates,
            // although the candidates may no longer be interested.
            return state == 'N' || state == 'CI' || state == 'DE';
        },
        can_decline() {
            let state = this.match.state;
            return state == 'N' || state == 'CI' || state == 'EI' || state == 'P';
        },
        can_make_job_offer() {
            return this.match.state == 'P';
        },
        can_withdraw_job_offer() {
            return this.match.state == 'JO';
        },
        no_action_possible() {
            let state = this.match.state;
            return state == 'DC' || state == 'H' || state == 'JD' || state == 'F' || state == 'W';
        },
        education_name() {
            return ss.education_names[this.match.candidate.highest_education];
        },
        real_avatar_path() {
            if (this.match.candidate.photo == '')
                return null;
            return API_HOST + '/api/download/' + this.match.candidate.user.id + '/' + this.match.candidate.photo
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
        make_job_offer() {
            var user = this.match.candidate.user;
            if (!confirm("Are you sure that you want to offer the job " + this.match.job.name
                + " to " + user.first_name + " " + user.last_name
                 + "? If the candidate accepts, this action cannot be undone."))
                return;
            axios({
                method: 'post',
                url: API_HOST + '/api/job-matches/' + this.match.id + '/make_job_offer/'
            }).then((response) => {
                if (response.status === 200 || response.status === 201) {
                    this.match.state = response.data.state;
                }
            }).catch(function (error) {
                alert(error.response.data)
            })
        },
        withdraw_job_offer() {
            var user = this.match.candidate.user;
            if (!confirm("Are you sure that you want to withdraw your offer of the job " + this.match.job.name
                + " to " + user.first_name + " " + user.last_name + "?"))
                return;
            axios({
                method: 'post',
                url: API_HOST + '/api/job-matches/' + this.match.id + '/withdraw_job_offer/'
            }).then((response) => {
                if (response.status === 200 || response.status === 201) {
                    this.match.state = response.data.state;
                }
            }).catch(function (error) {
                alert(error.response.data)
            })
        },
        view_details() {
            this.$emit('candidate_clicked', this.match.candidate);
        }
    }
}
</script>

<!-- CSS -->
<style lang="scss">
@import '../assets/css/skillstash.css';

.media {
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-align: start;
    -ms-flex-align: start;
    align-items: flex-start;
}

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
