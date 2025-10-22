<template>
    <form @submit.prevent="sendFiles" action="#">
        <h1>images:</h1>
        <input ref="files_input" type="file" multiple placeholder="Files" name="files"></input>
        <button type="submit">Submit</button>
        <img ref="img_el"></img>
    </form>
</template>

<script setup lang="ts">
import { useTemplateRef } from 'vue';

// fetch('')

const img_el = useTemplateRef<HTMLImageElement>('img_el')
const files_input = useTemplateRef('files_input')

async function sendFiles() {
    const formData = new FormData();

    const files = files_input.value?.files;

    if (files) {
        formData.append('file', files[0]);

        const response = await fetch('http://127.0.0.1:8000/echo-image', {
            method: 'POST',
            body: formData
        });
        const blob = await response.blob()
        const url_data = URL.createObjectURL(blob)
        img_el.value!.src = url_data

        console.log(response);
    }
        
}
</script>

<style scoped>
</style>
