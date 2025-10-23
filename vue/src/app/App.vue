<template>
    <form class="form" @submit.prevent="sendFiles" action="#">
        <div class="header">
            <h1 class="title">Картинки</h1>

            <input ref="files_input" type="file" multiple placeholder="Files" name="files" />

            <button type="submit">Отправить</button>
        </div>

        <div class="list">
            <img class="img" v-for="img in images" :key="img.id" :src="img.url" />
        </div>
    </form>
</template>

<script setup lang="ts">
import { ref, useTemplateRef } from "vue";

// fetch('')

const images = ref<{ id: number, url: string }[]>([])

// const img_el = useTemplateRef<HTMLImageElement>("img_el");
const files_input = useTemplateRef("files_input");

async function sendFiles() {
    const formData = new FormData();

    const files = files_input.value?.files;

    if (files) {
        [...files].forEach((file: Blob) => {
            formData.append("files", file);
        });

        const response = await fetch("http://147.45.107.168:8080/echo-image", {
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

<style scoped>
.form {
    display: grid;
    gap: 1rem;
}
.header {
    background-color: rgb(235, 183, 71);
    padding: 1rem;
    border-radius: 5px;
}
.list {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    width: 100%;
    gap: 1rem;
}

.img {
    min-width: 0;
    min-height: 0;
    width: 100%;
    object-fit: cover;
    height: 200px;
    border-radius: 5px;
}

.title {
    /* color: #548bba; */
}
/* Стили для кнопки */
button[type="submit"] {
    padding: 12px 24px;
    background: #228be6;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    align-self: flex-start;
}

button[type="submit"]:hover {
    background: #1c7ed6;
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(34, 139, 230, 0.3);
}

button[type="submit"]:active {
    transform: translateY(0);
}

button[type="submit"]:disabled {
    background: #adb5bd;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
}


/* Альтернативный стиль для input файлов */
.file-input-wrapper {
    position: relative;
    overflow: hidden;
    display: inline-block;
}

.file-input-wrapper input[type=file] {
    position: absolute;
    left: 0;
    top: 0;
    opacity: 0;
    cursor: pointer;
}

.custom-file-button {
    display: inline-block;
    padding: 12px 24px;
    background: #495057;
    color: white;
    border-radius: 6px;
    cursor: pointer;
    transition: background 0.3s ease;
}

.custom-file-button:hover {
    background: #343a40;
}
</style>
