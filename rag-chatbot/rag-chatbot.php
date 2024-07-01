<?php
/*
Plugin Name: RAG Chatbot
Description: A plugin to fetch WordPress posts for the RAG Chatbot.
Version: 1.0
Author: Vaibhav
*/

if (!defined('ABSPATH')) {
    exit;
}

class RAG_Chatbot {
    public function __construct() {
        add_action('save_post', array($this, 'fetch_post_data'));
        add_action('rest_api_init', function () {
            register_rest_route('rag-chatbot/v1', '/posts/', array(
                'methods' => 'GET',
                'callback' => array($this, 'get_all_posts'),
            ));
        });
    }

    public function fetch_post_data($post_id) {
        $post = get_post($post_id);
        if ($post->post_status == 'publish') {
            $content = array(
                'ID' => $post->ID,
                'title' => $post->post_title,
                'content' => $post->post_content,
                'date' => $post->post_date,
            );
            $this->send_post_to_api($content);
        }
    }

    public function send_post_to_api($post_data) {
        $response = wp_remote_post('http://localhost:5000/update_embeddings', array(
            'method' => 'POST',
            'body' => json_encode($post_data),
            'headers' => array(
                'Content-Type' => 'application/json',
            ),
        ));
    }

    public function get_all_posts() {
        $args = array(
            'numberposts' => -1,
            'post_status' => 'publish',
        );
        $posts = get_posts($args);
        $data = array();

        foreach ($posts as $post) {
            $data[] = array(
                'ID' => $post->ID,
                'title' => $post->post_title,
                'content' => $post->post_content,
                'date' => $post->post_date,
            );
        }
        return $data;
    }
}

new RAG_Chatbot();
