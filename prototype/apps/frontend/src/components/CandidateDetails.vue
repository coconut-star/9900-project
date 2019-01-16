<!-- CandidateDetails component -->
<template>
<div class="candidate-details">
    <!-- Header. -->
    <div class="candidate-header">
        <h2>{{candidate.user.first_name}} {{candidate.user.last_name}}</h2>
        <span @click="close_details" class="glyphicon glyphicon-remove pull-right"></span>
    </div>
    <!-- Main info. -->
    <div class="paper-up">
        <div class="profile-avatar-col paper-left">
            <img :src="real_avatar_path" v-if="real_avatar_path" alt="..." class="img-circle profile_img">
            <img src="../assets/images/default.png" v-else alt="..." class="img-circle profile_img">
        </div>
        <div class="info-col paper-right card-body">
            <table>
                <tr>
                    <td>
                        <i class="fa fa-envelope"></i><label class="info-label">E-mail:</label>
                        {{candidate.user.email}}
                    </td>
                </tr>
                <tr>
                    <td>
                        <i class="fa fa-phone"></i><label class="info-label">Phone:</label>
                        {{candidate.user.phone}}
                    </td>
                </tr>
                <tr>
                    <td>
                        <i class="fa fa-map-marker"></i><label class="info-label">City:</label>
                        {{candidate.user.city}}
                    </td>
                </tr>
                <tr>
                    <td>
                        <i class="fa fa-calendar"></i><label class="info-label">Date of Birth:</label>
                        {{candidate.date_of_birth}}
                    </td>
                </tr>
                <tr>
                    <td>
                        <i class="fa fa-user"></i><label class="info-label">Gender:</label>
                        {{gender_name}}
                    </td>
                </tr>
                <tr>
                    <td>
                        <i class="fa fa-graduation-cap"></i><label class="info-label">Education:</label>
                        {{education_name}}
                    </td>
                </tr>
                <tr>
                    <td>
                        <i class="fa fa-money"></i><label class="info-label">Minimum Salary:</label>
                        {{candidate.minimum_salary}}
                    </td>
                </tr>
                <tr>
                    <td>
                        <i class="fa fa-calendar"></i><label class="info-label">Joined On:</label>
                        {{candidate.user.date_joined}}
                    </td>
                </tr>
                <tr>
                    <td v-if="candidate.looking_for_work">Currently looking for work</td>
                    <td v-else>Not currently looking for work</td>
                </tr>              
            </table>
        </div>
    </div>

    <!-- Skill info. -->
    <div class="paper-down">
        <div class="col-md-10 col-md-offset-1 col-lg-10 col-lg-offset-1">
            <h3>Skills</h3>
            <table class="skill-table">
                <thead>
                    <tr>
                        <th>Skill</th>
                        <th>Proficiency</th>
                        <th>Experience</th>
                        <th>Evidence</th>
                    </tr>
                </thead>
                <tr v-for="(cs,index) in candidate_skills" :key="index">
                    <td>{{cs.skill.name}}</td>
                    <td>{{cs.proficiency}}</td>
                    <td v-if="cs.experience > 0 && cs.experience_unit == 12">{{cs.experience}} Years</td>
                    <td v-else-if="cs.experience > 0">{{cs.experience}} Months</td>
                    <td v-else></td>
                    <td>
                        <a v-for="(doc,index) in cs.evidence" :key="index" :href="doc.url">
                            {{doc.filename}}
                        </a>
                    </td>
                </tr>
            </table>
        </div>
    </div>
</div>
</template>

<!-- JavaScript -->
<script>
import axios from 'axios'
import * as ss from '../assets/js/skillstash.js';
export default {
    name: 'CandidateDetails',
    props: ['candidate'],
    data() {
        return {
            c_id: -1,
            c_skills: null
        }
    },
    computed: {
        candidate_skills() {
            if (this.c_id != this.candidate.user.id) {
                var docs = new Map();
                axios({
                    method: "get",
                    url: API_HOST + "/api/candidate-docs/",
                    params: {
                        candidate: this.candidate.user.id
                    }
                }).then(response => {
                    // Create a map from doc id to object.
                    for (let i in response.data) {
                        let doc = response.data[i];
                        docs.set(doc.id, doc);
                    }

                    axios({
                        method: "get",
                        url: API_HOST + "/api/candidate-skills/",
                        params: {
                            candidate: this.candidate.user.id
                        }
                    }).then(response => {
                        this.c_skills = response.data;
                        for (let i in this.c_skills) {
                            let cs = this.c_skills[i];
                            let evidence_docs = [];
                            for (let j in cs.evidence) {
                                let doc = docs.get(cs.evidence[j]);
                                if (doc != undefined) {
                                    doc.url = API_HOST + "/api/download/" + this.candidate.user.id + "/" + doc.filename;
                                    evidence_docs.push(doc);
                                }
                            }
                            cs.evidence = evidence_docs;
                        }
                    });
                });
                this.c_id = this.candidate.user.id;
            }
            return this.c_skills;
        },
        education_name() {
            return ss.education_names[this.candidate.highest_education];
        },
        gender_name() {
            if (this.candidate.gender == 'U') {
                return 'Unspecified';
            }
            return this.candidate.gender == 'M' ? 'Male' : 'Female';
        },
        real_avatar_path() {
            if (this.candidate.photo == '') {
                return null;
            }
            return API_HOST + '/api/download/' + this.candidate.user.id + '/' + this.candidate.photo;
        }
    },
    methods: {
        close_details() {
            this.$emit('close_clicked');
        }
    }
}
</script>

<!-- CSS -->
<style>
@import 'font-awesome/css/font-awesome.min.css';
@import '../../static/assets/css/build.css';
@import '../../static/assets/css/normalize.css';
@import '../../static/assets/css/themify-icons.css';
@import '../../static/assets/css/cs-skin-elastic.css';
@import '../assets/css/skillstash.css';
</style>
