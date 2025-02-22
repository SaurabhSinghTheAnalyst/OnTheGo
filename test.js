const axios = require('axios');

async function generatePodcast() {
    try {
        const response = await axios.post('http://localhost:8000/generate-podcast', {
            companies: ['Apple', 'Google'],
            output_file: 'tech_podcast.mp3'
        });
        console.log(response.data);
    } catch (error) {
        console.error('Error generating podcast:', error.response.data);
    }
}

generatePodcast();