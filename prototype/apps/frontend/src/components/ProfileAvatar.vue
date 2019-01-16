<template>
<div class="profile-pic">
    <img @click="update_avatar" :src="avatar_photo" v-if="avatar_photo" alt="..." class="img-circle profile_img">
    <img @click="update_avatar" src="../assets/images/default.png" v-else alt="..." class="img-circle profile_img">
    <div @click="update_avatar" class="edit"><a href="#"><i class="fa fa-plus fa-lg"></i></a></div>
    <button id="remove-photo" type="button" class="btn" @click='remove_photo' v-if="avatar_photo">Remove Avatar</button>
    <div class="form-group has-feedback" hidden>
        <input @change="avatar_changed_handler" id="photo" type="file" accept="image/*" />
    </div>
</div>
</template>

<script>
import axios from 'axios'
import $ from 'jquery'
export default {
    name: 'ProfileAvatar',
    props: ['profile_photo'],
    data() {
        return {
            initialized: false,
            aphoto: null
        }
    },
    computed: {
        avatar_photo: {
            get: function () {
                // This strange code is necessary because this method may be
                // called before this.profile_photo is set.
                if (!this.initialized && this.profile_photo) {
                    this.aphoto = this.profile_photo;
                    this.initialized = true;
                }
                return this.aphoto;
            },
            set: function (value) {
                this.aphoto = value;
            }
        }
    },
    methods: {
        update_avatar() {
            $('#photo').click();
        },
        avatar_changed_handler() {
            var photo_field = document.getElementById("photo")
            if (photo_field.files.length > 0) {
                this.upload_photo(photo_field.files[0])
            }
        },
        upload_photo(file) {
            const file_data = new FormData();
            file_data.append('file', file, file.name);
            axios({
                method: 'put',
                url: API_HOST + '/api/photo-upload/' + file.name,
                data: file_data
            }).then(response => {
                if (response.status >= 200 && response.status <=  205) {
                    this.avatar_photo = API_HOST + '/api/download/' + sessionStorage.getItem("user_id") + '/' + file.name
                    this.$emit('avatar_changed',this.avatar_photo);
                }
            }).catch(function (error) {
                alert(error.response.data)
            })
        },
        remove_photo() {
            if (!confirm('Are you sure you want to remove your profile photo?'))
                return false;
            // Split the URL and take just the filename.
            let components = this.profile_photo.split('/');
            let filename = components[components.length - 1]
            axios({
                method: 'delete',
                url: API_HOST + '/api/photo-upload/' + filename,
            }).then(response => {
                if (response.status >= 200 && response.status <=  205) {
                    this.avatar_photo = null;
                    this.$emit('avatar_changed', null);
                }
            }).catch(function (error) {
                alert(error.response.data)
            })
        }
    },
}
</script>

<style>
.img-circle.profile_img {
    width: 126px;
    background: #fff;
    margin-left: 15%;
    z-index: 1000;
    position: inherit;
    margin-top: 20px;
    border: 1px solid rgba(52, 73, 94, .44);
    padding: 4px;
}

#remove-photo {
    margin-left: 15%;
    margin-top: 20px;
}

.profile-pic {
	position: relative;
	display: inline-block;
}

.profile-pic:hover .edit {
	display: block;
}

.edit {
    padding-top: 7px;
    padding-right: 7px;
    position: absolute;
    right: 30px;
    top: 65px;
    z-index: 9999;
	display: none;
}

.edit a {
	color: #000;
}

</style>
