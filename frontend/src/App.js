import React, { useEffect, useState } from 'react';
import axios from 'axios';

const API_BASE_URL = 'https://hf513j4h9g.execute-api.ap-northeast-2.amazonaws.com/production/api';

function App() {
  return (
    <div>
      <h1>Diary App</h1>
      <CreateDiary />
      <ListDiaries />
    </div>
  );
}

function ListDiaries() {
  const [diaries, setDiaries] = useState([]);

  // API를 호출하여 다이어리 목록을 가져옴
  useEffect(() => {
    axios.get(`${API_BASE_URL}/list`)
      .then((response) => setDiaries(response.data))
      .catch((error) => console.error('Error fetching diaries:', error));
  }, []);

  // 다이어리 삭제
  const deleteDiary = (id) => {
    axios.delete(`${API_BASE_URL}/delete/${id}`)
      .then(() => setDiaries(diaries.filter(diary => diary.id !== id)))
      .catch((error) => console.error('Error deleting diary:', error));
  };

  return (
    <div>
      <h2>Diary List</h2>
      <ul>
        {diaries.map((diary) => (
          <li key={diary.id}>
            <h3>{diary.title}</h3>
            <p>{diary.content}</p>
            <button onClick={() => deleteDiary(diary.id)}>Delete</button>
            <UpdateDiary diary={diary} />
          </li>
        ))}
      </ul>
    </div>
  );
}

function CreateDiary() {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');

  // 새로운 다이어리 작성
  const handleSubmit = (event) => {
    event.preventDefault();
    axios.post(`${API_BASE_URL}/diaries`, { title, content })
      .then((response) => {
        console.log('Diary created:', response.data);
        setTitle('');
        setContent('');
        window.location.reload();  // 새로고침하여 목록 업데이트
      })
      .catch((error) => console.error('Error creating diary:', error));
  };

  return (
    <div>
      <h2>Create New Diary</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Title:</label>
          <input value={title} onChange={(e) => setTitle(e.target.value)} required />
        </div>
        <div>
          <label>Content:</label>
          <textarea value={content} onChange={(e) => setContent(e.target.value)} required />
        </div>
        <button type="submit">Create</button>
      </form>
    </div>
  );
}

function UpdateDiary({ diary }) {
  const [title, setTitle] = useState(diary.title);
  const [content, setContent] = useState(diary.content);

  // 다이어리 업데이트
  const handleUpdate = (event) => {
    event.preventDefault();
    axios.put(`${API_BASE_URL}/diaries/${diary.id}`, { title, content })
      .then((response) => {
        console.log('Diary updated:', response.data);
        window.location.reload();  // 새로고침하여 목록 업데이트
      })
      .catch((error) => console.error('Error updating diary:', error));
  };

  return (
    <div>
      <h4>Update Diary</h4>
      <form onSubmit={handleUpdate}>
        <div>
          <label>Title:</label>
          <input value={title} onChange={(e) => setTitle(e.target.value)} />
        </div>
        <div>
          <label>Content:</label>
          <textarea value={content} onChange={(e) => setContent(e.target.value)} />
        </div>
        <button type="submit">Update</button>
      </form>
    </div>
  );
}

export default App;
