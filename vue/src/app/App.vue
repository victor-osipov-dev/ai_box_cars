<template>
    <form class="form" @submit.prevent="sendFiles" action="#">
        <div class="header">
            <h1 class="title">Картинки</h1>

            <input
                @change="selectFiles"
                ref="files_input"
                type="file"
                multiple
                placeholder="Files"
                name="files"
            />

            <div class="header__bottom">
                <button class="button" type="submit">Отправить</button>
                <img class="loading" src="/loading.png" v-if="isLoading" />
            </div>
        </div>

        <details v-if="fake_data">
            <summary>Прикреплённые файлы</summary>
            <div class="fake_imgs">
                <img class="img_fake" v-for="img in files_list" :src="img" />
            </div>
        </details>

        <div class="list">
            <img
                class="img"
                v-for="img in images"
                :key="img.id"
                :src="img.url"
            />
            <img
                v-if="submit_fake_data"
                class="img_fake"
                v-for="img in files_list_result"
                :src="img"
            />
        </div>
    </form>
</template>

<script setup lang="ts">
import { ref, useTemplateRef } from "vue";

const files_list = ["1.jpg", "3.jpg", "4.jpg"];
const files_list_result = ["11.jpg", "33.jpg", "44.jpg"];

const images = ref<{ id: number; url: string }[]>([]);
const files_input = useTemplateRef("files_input");
const fake_data = ref(true);
const submit_fake_data = ref(false);
const isLoading = ref(false);

function selectFiles() {
    console.log(123);

    fake_data.value = files_input.value?.files?.length == 0 ? true : false;
}

async function sendFiles() {
    const formData = new FormData();

    const files = files_input.value?.files;

    if (files?.length !== 0) {
        [...files].forEach((file: Blob) => {
            formData.append("files", file);
        });

        isLoading.value = true;

        const response = await fetch("http://147.45.107.168:8080/echo-image", {
            method: "POST",
            body: formData,
        });
        const form_data = await response.formData();
        const form_data_files = form_data.getAll("image") as File[];

        images.value = form_data_files.map((file: File, index) => ({
            id: index,
            url: URL.createObjectURL(file),
        }));

        isLoading.value = false;
    } else {
        submit_fake_data.value = true;
    }
}
</script>

<style scoped>
.header__bottom {
    display: flex;
    align-items: center;
    margin-top: 1rem;
    gap: 1rem;
}
.loading {
    animation: spin 2s linear infinite;
    width: 40px;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(360deg);
    }
}

details {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 0;
    margin: 10px 0;
    background: #fafafa;
    transition: all 0.3s ease;
}

details[open] {
    background: #ffffff;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

summary {
    padding: 12px 16px;
    cursor: pointer;
    font-weight: 500;
    color: #333;
    list-style: none;
    position: relative;
    user-select: none;
}

/* Убираем стандартный маркер */
summary::-webkit-details-marker {
    display: none;
}

/* Кастомный маркер */
summary::after {
    content: "▶";
    position: absolute;
    right: 16px;
    top: 50%;
    transform: translateY(-50%) rotate(0deg);
    transition: transform 0.3s ease;
    color: #666;
}

details[open] summary::after {
    transform: translateY(-50%) rotate(90deg);
}

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

.img_fake {
    width: 100%;
    max-width: 400px;
    width: 100%;
    height: 200px;
    object-fit: cover;
}
.fake_imgs {
    display: flex;
    flex-wrap: wrap;
    padding: 1rem;
    gap: 1rem;
}
.title {
    /* color: #548bba; */
    margin-bottom: 0.5rem;
}
/* Стили для кнопки */
.button {
    /* margin-top: 1rem; */
}
.button[type="submit"] {
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

.button[type="submit"]:hover {
    background: #1c7ed6;
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(34, 139, 230, 0.3);
}

.button[type="submit"]:active {
    transform: translateY(0);
}

.button[type="submit"]:disabled {
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

.file-input-wrapper input[type="file"] {
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
