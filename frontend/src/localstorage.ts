export default {
  set(key: string, value: any) {
    localStorage.setItem(key, JSON.stringify(value));
  },

  get(key:string): any {
    const value = localStorage.getItem(key);
    return value ? JSON.parse(value) : null;
  },

  remove(key:string) {
    localStorage.removeItem(key);
  },

  clear() {
    localStorage.clear();
  }
}