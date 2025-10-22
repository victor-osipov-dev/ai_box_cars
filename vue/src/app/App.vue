<template>
    <form @submit.prevent="sendFiles" action="#">
        <h1>images:</h1>
        <input ref="files_input" type="file" multiple placeholder="Files" name="files" />
        <button type="submit">Submit</button>
        <img v-for="img in images" :key="img.id" :src="img.url"/>
    </form>
</template>

<script setup lang="ts">
import { ref, useTemplateRef } from "vue";

// fetch('')

const images = ref<{id: number, url: string}[]>([])

// const img_el = useTemplateRef<HTMLImageElement>("img_el");
const files_input = useTemplateRef("files_input");

async function sendFiles() {
    const formData = new FormData();

    const files = files_input.value?.files;

    if (files) {
        [...files].forEach((file: Blob) => {
            formData.append("files", file);
        });
        
        const response = await fetch("http://127.0.0.1:8000/echo-image", {
            method: "POST",
            body: formData,
        });
        const form_data = await response.formData();
        const form_data_files = form_data.getAll('image') as File[]
        
        // const url_data = URL.createObjectURL(form_data.get('image') as Blob);
        // img_el.value!.src = url_data;

        images.value = form_data_files.map((file: File, index) => ({
            id: index,
            url: URL.createObjectURL(file)
        }))

        // console.log(response);
    }
}
</script>

<style scoped></style>
