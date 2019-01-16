<template>
<div class="candidate-details">
    <div class="candidate-header">
        <h2>{{job.name}}</h2>
        <span @click="close_details" class="glyphicon glyphicon-remove pull-right"></span>
    </div>
    <div class="paper-up">
        <div class="profile-avatar-col paper-left">
            <img :src="real_avatar_path" v-if="real_avatar_path" alt="..." class="img-circle profile_img">
            <img src="../assets/images/default.png" v-else alt="..." class="img-circle profile_img">
        </div>
        <div class="candidate-info paper-right card-body">
            <table>
                <tr>
                    <td>
                        <i class="fa fa-tasks"></i><label class="info-label">Description:</label>
                        {{job.description}}
                    </td>
                </tr>
                <tr>
                    <td>
                        <i class="fa fa-building"></i><label class="info-label">Company:</label>
                        {{job.contact_person.company}}
                    </td>
                </tr>
                <tr>
                    <td>
                        <i class="fa fa-map-marker"></i><label class="info-label">City:</label>
                        {{job.city}}
                    </td>
                </tr>
                <tr>
                    <td>
                        <i class="fa fa-money"></i><label class="info-label">Pay:</label>
                        {{salary}}
                    </td>
                </tr>
                <tr>
                    <td>
                        <i class="fa fa-user"></i><label class="info-label">Contact Person:</label>
                        {{job.contact_person.user.first_name}} {{job.contact_person.user.last_name}}
                    </td>
                </tr>
                <tr>
                    <td>
                        <i class="fa fa-envelope"></i><label class="info-label">Email:</label>
                        {{job.contact_person.user.email}}
                    </td>
                </tr>
                 <tr>
                    <td>
                        <i class="fa fa-phone"></i><label class="info-label">Phone:</label>
                        {{job.contact_person.user.phone}}
                    </td>
                </tr>
                <tr>
                    <td>
                        <i class="fa fa-graduation-cap"></i><label class="info-label">Required Education:</label>
                        {{education_name}}
                    </td>
                </tr>
                <tr>
                    <td>
                        <i class="fa fa-calendar"></i><label class="info-label">Date Posted:</label>
                        {{job.date_posted}}
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="paper-down">
        <div class="col-md-10 col-md-offset-1 col-lg-10 col-lg-offset-1">
            <h3>Relevant Skills</h3>
            <table class="skill-table">
                <thead>
                    <tr>
                        <th>Skill</th>
                        <th>Proficiency</th>
                        <th>Experience</th>
                    </tr>
                </thead>
                <tr v-for="(js,index) in job_skills" :key="index">
                    <td>{{js.skill.name}}</td>
                    <td>{{js.proficiency}}</td>
                    <td v-if="js.experience > 0 && js.experience_unit == 12">{{js.experience}} Years</td>
                    <td v-else-if="js.experience > 0">{{js.experience}} Months</td>
                    <td v-else></td>
                </tr>
            </table>
        </div>
    </div>
</div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'JobDetails',
    props: ['job'],
    data() {
        return {
            j_id: -1,
            j_skills: null
        }
    },
    computed: {
        job_skills() {
            if (this.j_id != this.job.id) {
                axios({
                    method: "get",
                    url: API_HOST + "/api/job-skills/",
                    params: {
                        job: this.job.id
                    }
                }).then(response => {
                    this.j_skills = response.data;
                });
                this.j_id = this.job.id;
            }
            return this.j_skills;
        },
        education_name() {
            var qualifications = [
                "No Requirement",
                "High School",
                "Certificate",
                "Associate Diploma",
                "Diploma",
                "Bachelor's Degree",
                "Graduate Certificate",
                "Graduate Diploma",
                "Master's Degree",
                "Ph.D"
            ];
            return qualifications[this.job.required_education];
        },
        real_avatar_path() {
            if (this.job.contact_person.photo == '') {
                return null;
            }
            return API_HOST + '/api/download/' + this.job.contact_person.user.id + '/' + this.job.contact_person.photo;
        },
        salary() {
            let pay_type = this.job.pay_type;
            let pay_period = '';
            if (pay_type === 'D')
                pay_period = 'Day';
            else if (pay_type === 'H')
                pay_period = 'Hour';
            else if (pay_type === 'M')
                pay_period = 'Month';
            else if (pay_type === 'Y')
                pay_period = 'Year';
            return '$' + this.job.pay + ' / ' + pay_period;
        }
    },
    methods: {
        close_details() {
            this.$emit('close_clicked');
        }
    }
}
</script>

<style>
@import 'font-awesome/css/font-awesome.min.css';
@import '../../static/assets/css/build.css';
@import '../../static/assets/css/normalize.css';
@import '../../static/assets/css/themify-icons.css';
@import '../../static/assets/css/cs-skin-elastic.css';
@import '../assets/css/skillstash.css';

</style>
