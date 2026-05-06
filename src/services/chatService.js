import { dbPaths } from '../config/paths.js';
import { pushPath, updatePath } from './firebaseDb.js';

export function createChannel(channel) {
  const now = Date.now();
  return pushPath(dbPaths.chatChannels, {
    ...channel,
    createdAt: now,
    updatedAt: now
  });
}

export function sendMessage(channelId, message) {
  return pushPath(`${dbPaths.chatMessages}/${channelId}`, {
    ...message,
    createdAt: Date.now(),
    editedAt: null,
    deleted: false
  });
}

export function markChannelRead(channelId, userId) {
  return updatePath(`${dbPaths.chatReads}/${channelId}/${userId}`, {
    lastReadAt: Date.now()
  });
}
