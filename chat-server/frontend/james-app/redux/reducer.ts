import { combineReducers } from "@reduxjs/toolkit";
import { persistReducer } from "redux-persist";
import countReducer from "@/app/components/counter/service/counter-slice";
import articleReducer from "@/app/components/article/service/article-slice";
import createWebStorage from "redux-persist/lib/storage/createWebStorage";
import userReducer from "@/app/components/user/service/user-slice"
import boardReducer from "@/app/components/board/service/board-slice"


const createNoopStorage = () => {
  return {
    getItem() {
      return Promise.resolve(null);
    },
    setItem(_key: string, value: number) {
      return Promise.resolve(value);
    },
    removeItem() {
      return Promise.resolve();
    },
  };
};

const storage =
  typeof window !== "undefined"
    ? createWebStorage("local")
    : createNoopStorage();

const countPersistConfig = {    // 상태는 키 값이다 = count
  key: "count",                 // key = 상태 -> 리액트가 무상태이고 리덕스는 상태가 있다.
  whitelist: ["countState"],    // 리액트가 템플릿을 잡아주고 리덕스가 데이터를 뿌려준다.
  storage,                      // ex) 상태가 있는 것 = 책, 상태가 없는 것 = e북
};
const articlePersistConfig = {
  key: "article",
  storage,
  whitelist: ["articleState"],
};
const userPersistConfig = {
  key: "user",
  storage,
  whitelist: ["userState"],
};
const boardPersistConfig = {
  key: "board",
  storage,
  whitelist: ["boardState"],
};


const persistedCountReducer = persistReducer(countPersistConfig, countReducer);
const persistedArticleReducer = persistReducer(articlePersistConfig, articleReducer);
const persistedUserReducer = persistReducer(userPersistConfig, userReducer)
const persistedBoardReducer = persistReducer(boardPersistConfig, boardReducer)

export const rootReducer = combineReducers({  // combineReducers({})는 키(상태)를 합치는 것
  count: persistedCountReducer,               // count, article, user
  article: persistedArticleReducer,
  user: persistedUserReducer,
  board: persistedBoardReducer
});