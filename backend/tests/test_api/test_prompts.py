"""
API Tests for Prompts endpoint
"""

import pytest
from fastapi import status


class TestPromptsAPI:
    """Тесты для /api/prompts endpoints"""
    
    def test_get_prompts_empty(self, client):
        """Тест получения пустого списка промптов"""
        response = client.get("/api/prompts")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []
    
    def test_create_prompt(self, client, sample_prompt_data):
        """Тест создания нового промпта"""
        response = client.post("/api/prompts", json=sample_prompt_data)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["title"] == sample_prompt_data["title"]
        assert data["content"] == sample_prompt_data["content"]
        assert data["category"] == sample_prompt_data["category"]
        assert "id" in data
    
    def test_create_prompt_missing_title(self, client, sample_prompt_data):
        """Тест создания промпта без названия"""
        invalid_data = sample_prompt_data.copy()
        del invalid_data["title"]
        
        response = client.post("/api/prompts", json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_prompt_missing_content(self, client, sample_prompt_data):
        """Тест создания промпта без содержимого"""
        invalid_data = sample_prompt_data.copy()
        del invalid_data["content"]
        
        response = client.post("/api/prompts", json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_get_prompt_by_id(self, client, sample_prompt_data):
        """Тест получения промпта по ID"""
        # Создаём промпт
        create_response = client.post("/api/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        # Получаем промпт
        response = client.get(f"/api/prompts/{prompt_id}")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["id"] == prompt_id
        assert data["title"] == sample_prompt_data["title"]
    
    def test_get_nonexistent_prompt(self, client):
        """Тест получения несуществующего промпта"""
        response = client.get("/api/prompts/99999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_prompt(self, client, sample_prompt_data):
        """Тест удаления промпта"""
        # Создаём промпт
        create_response = client.post("/api/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        # Удаляем промпт
        response = client.delete(f"/api/prompts/{prompt_id}")
        assert response.status_code == status.HTTP_200_OK
        
        # Проверяем что промпт удалён
        get_response = client.get(f"/api/prompts/{prompt_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_update_prompt(self, client, sample_prompt_data):
        """Тест обновления промпта"""
        # Создаём промпт
        create_response = client.post("/api/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        # Обновляем промпт
        updated_data = sample_prompt_data.copy()
        updated_data["title"] = "Updated Title"
        updated_data["content"] = "Updated content"
        
        response = client.put(f"/api/prompts/{prompt_id}", json=updated_data)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["title"] == updated_data["title"]
        assert data["content"] == updated_data["content"]


class TestPromptsFiltering:
    """Тесты фильтрации промптов"""
    
    def test_filter_by_category(self, client, sample_prompt_data):
        """Тест фильтрации по категории"""
        # Создаём несколько промптов разных категорий
        prompt1 = sample_prompt_data.copy()
        prompt1["category"] = "general"
        client.post("/api/prompts", json=prompt1)
        
        prompt2 = sample_prompt_data.copy()
        prompt2["category"] = "technical"
        prompt2["title"] = "Technical Prompt"
        client.post("/api/prompts", json=prompt2)
        
        # Фильтруем по категории
        response = client.get("/api/prompts?category=technical")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert len(data) >= 1
        for prompt in data:
            assert prompt["category"] == "technical"
