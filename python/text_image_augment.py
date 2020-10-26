#coding: utf-8
import math

import numpy as np

class WarpMLS:
    def __init__(self, src, src_pts, dst_pts, dst_w, dst_h, trans_ratio=1.):
        self.src = src
        self.src_pts = src_pts
        self.dst_pts = dst_pts
        self.pt_count = len(self.dst_pts)
        self.dst_w = dst_w
        self.dst_h = dst_h
        self.trans_ratio = trans_ratio
        self.grid_size = 100
        self.rdx = np.zeros((self.dst_h, self.dst_w))
        self.rdy = np.zeros((self.dst_h, self.dst_w))

    @staticmethod
    def __bilinear_interp(x, y, v11, v12, v21, v22):
        return (v11 * (1 - y) + v12 * y) * (1 - x) + (v21 * (1 - y) + v22 * y) * x

    def generate(self):
        self.calc_delta()
        return self.gen_img()

    def calc_delta(self):
        w = np.zeros(self.pt_count, dtype=np.float32)

        if self.pt_count < 2:
            return

        i = 0
        while 1:
            if self.dst_w <= i < self.dst_w + self.grid_size - 1:
                i = self.dst_w - 1
            elif i >= self.dst_w:
                break

            j = 0
            while 1:
                if self.dst_h <= j < self.dst_h + self.grid_size - 1:
                    j = self.dst_h - 1
                elif j >= self.dst_h:
                    break

                sw = 0
                swp = np.zeros(2, dtype=np.float32)
                swq = np.zeros(2, dtype=np.float32)
                new_pt = np.zeros(2, dtype=np.float32)
                cur_pt = np.array([i, j], dtype=np.float32)

                k = 0
                for k in range(self.pt_count):
                    if i == self.dst_pts[k][0] and j == self.dst_pts[k][1]:
                        break

                    w[k] = 1. / ((i - self.dst_pts[k][0]) * (i - self.dst_pts[k][0]) +
                                 (j - self.dst_pts[k][1]) * (j - self.dst_pts[k][1]))

                    sw += w[k]
                    swp = swp + w[k] * np.array(self.dst_pts[k])
                    swq = swq + w[k] * np.array(self.src_pts[k])

                if k == self.pt_count - 1:
                    pstar = 1 / sw * swp
                    qstar = 1 / sw * swq

                    miu_s = 0
                    for k in range(self.pt_count):
                        if i == self.dst_pts[k][0] and j == self.dst_pts[k][1]:
                            continue
                        pt_i = self.dst_pts[k] - pstar
                        miu_s += w[k] * np.sum(pt_i * pt_i)

                    cur_pt -= pstar
                    cur_pt_j = np.array([-cur_pt[1], cur_pt[0]])

                    for k in range(self.pt_count):
                        if i == self.dst_pts[k][0] and j == self.dst_pts[k][1]:
                            continue

                        pt_i = self.dst_pts[k] - pstar
                        pt_j = np.array([-pt_i[1], pt_i[0]])

                        tmp_pt = np.zeros(2, dtype=np.float32)
                        tmp_pt[0] = np.sum(pt_i * cur_pt) * self.src_pts[k][0] - \
                                    np.sum(pt_j * cur_pt) * self.src_pts[k][1]
                        tmp_pt[1] = -np.sum(pt_i * cur_pt_j) * self.src_pts[k][0] + \
                                    np.sum(pt_j * cur_pt_j) * self.src_pts[k][1]
                        tmp_pt *= (w[k] / miu_s)
                        new_pt += tmp_pt

                    new_pt += qstar
                else:
                    new_pt = self.src_pts[k]

                self.rdx[j, i] = new_pt[0] - i
                self.rdy[j, i] = new_pt[1] - j

                j += self.grid_size
            i += self.grid_size

    def gen_img(self):
        src_h, src_w = self.src.shape[:2]
        dst = np.zeros_like(self.src, dtype=np.float32)

        for i in np.arange(0, self.dst_h, self.grid_size):
            for j in np.arange(0, self.dst_w, self.grid_size):
                ni = i + self.grid_size
                nj = j + self.grid_size
                w = h = self.grid_size
                if ni >= self.dst_h:
                    ni = self.dst_h - 1
                    h = ni - i + 1
                if nj >= self.dst_w:
                    nj = self.dst_w - 1
                    w = nj - j + 1

                di = np.reshape(np.arange(h), (-1, 1))
                dj = np.reshape(np.arange(w), (1, -1))
                delta_x = self.__bilinear_interp(di / h, dj / w,
                                                 self.rdx[i, j], self.rdx[i, nj],
                                                 self.rdx[ni, j], self.rdx[ni, nj])
                delta_y = self.__bilinear_interp(di / h, dj / w,
                                                 self.rdy[i, j], self.rdy[i, nj],
                                                 self.rdy[ni, j], self.rdy[ni, nj])
                nx = j + dj + delta_x * self.trans_ratio
                ny = i + di + delta_y * self.trans_ratio
                nx = np.clip(nx, 0, src_w - 1)
                ny = np.clip(ny, 0, src_h - 1)
                nxi = np.array(np.floor(nx), dtype=np.int32)
                nyi = np.array(np.floor(ny), dtype=np.int32)
                nxi1 = np.array(np.ceil(nx), dtype=np.int32)
                nyi1 = np.array(np.ceil(ny), dtype=np.int32)

                dst[i:i + h, j:j + w] = self.__bilinear_interp(np.tile(np.expand_dims(ny - nyi, axis=-1), (1, 1, 3)),
                                                               np.tile(np.expand_dims(nx - nxi, axis=-1), (1, 1, 3)),
                                                               self.src[nyi, nxi],
                                                               self.src[nyi, nxi1],
                                                               self.src[nyi1, nxi],
                                                               self.src[nyi1, nxi1]
                                                               )

                # for di in range(h):
                #     for dj in range(w):
                #         # print(ni, nj, i, j)
                #         delta_x = self.__bilinear_interp(di / h, dj / w, self.rdx[i, j], self.rdx[i, nj],
                #                                          self.rdx[ni, j], self.rdx[ni, nj])
                #         delta_y = self.__bilinear_interp(di / h, dj / w, self.rdy[i, j], self.rdy[i, nj],
                #                                          self.rdy[ni, j], self.rdy[ni, nj])
                #         nx = j + dj + delta_x * self.trans_ratio
                #         ny = i + di + delta_y * self.trans_ratio
                #         nx = min(src_w - 1, max(0, nx))
                #         ny = min(src_h - 1, max(0, ny))
                #         nxi = int(nx)
                #         nyi = int(ny)
                #         nxi1 = math.ceil(nx)
                #         nyi1 = math.ceil(ny)
                #
                #         dst[i + di, j + dj] = self.__bilinear_interp(ny - nyi, nx - nxi,
                #                                                      self.src[nyi, nxi],
                #                                                      self.src[nyi, nxi1],
                #                                                      self.src[nyi1, nxi],
                #                                                      self.src[nyi1, nxi1]
                #                                                      )

        dst = np.clip(dst, 0, 255)
        dst = np.array(dst, dtype=np.uint8)

        return dst
    
def distort(src, segment):
    img_h, img_w = src.shape[:2]

    cut = img_w // segment
    thresh = cut // 3
    # thresh = img_h // segment // 3
    # thresh = img_h // 5

    src_pts = list()
    dst_pts = list()

    src_pts.append([0, 0])
    src_pts.append([img_w, 0])
    src_pts.append([img_w, img_h])
    src_pts.append([0, img_h])

    dst_pts.append([np.random.randint(thresh), np.random.randint(thresh)])
    dst_pts.append([img_w - np.random.randint(thresh), np.random.randint(thresh)])
    dst_pts.append([img_w - np.random.randint(thresh), img_h - np.random.randint(thresh)])
    dst_pts.append([np.random.randint(thresh), img_h - np.random.randint(thresh)])

    half_thresh = thresh * 0.5

    for cut_idx in np.arange(1, segment, 1):
        src_pts.append([cut * cut_idx, 0])
        src_pts.append([cut * cut_idx, img_h])
        dst_pts.append([cut * cut_idx + np.random.randint(thresh) - half_thresh,
                        np.random.randint(thresh) - half_thresh])
        dst_pts.append([cut * cut_idx + np.random.randint(thresh) - half_thresh,
                        img_h + np.random.randint(thresh) - half_thresh])

    trans = WarpMLS(src, src_pts, dst_pts, img_w, img_h)
    dst = trans.generate()

    return dst


def stretch(src, segment):
    img_h, img_w = src.shape[:2]

    cut = img_w // segment
    thresh = cut * 4 // 5
    # thresh = img_h // segment // 3
    # thresh = img_h // 5

    src_pts = list()
    dst_pts = list()

    src_pts.append([0, 0])
    src_pts.append([img_w, 0])
    src_pts.append([img_w, img_h])
    src_pts.append([0, img_h])

    dst_pts.append([0, 0])
    dst_pts.append([img_w, 0])
    dst_pts.append([img_w, img_h])
    dst_pts.append([0, img_h])

    half_thresh = thresh * 0.5

    for cut_idx in np.arange(1, segment, 1):
        move = np.random.randint(thresh) - half_thresh
        src_pts.append([cut * cut_idx, 0])
        src_pts.append([cut * cut_idx, img_h])
        dst_pts.append([cut * cut_idx + move, 0])
        dst_pts.append([cut * cut_idx + move, img_h])

    trans = WarpMLS(src, src_pts, dst_pts, img_w, img_h)
    dst = trans.generate()

    return dst


def perspective(src):
    img_h, img_w = src.shape[:2]

    thresh = img_h // 2

    src_pts = list()
    dst_pts = list()

    src_pts.append([0, 0])
    src_pts.append([img_w, 0])
    src_pts.append([img_w, img_h])
    src_pts.append([0, img_h])

    dst_pts.append([0, np.random.randint(thresh)])
    dst_pts.append([img_w, np.random.randint(thresh)])
    dst_pts.append([img_w, img_h - np.random.randint(thresh)])
    dst_pts.append([0, img_h - np.random.randint(thresh)])

    trans = WarpMLS(src, src_pts, dst_pts, img_w, img_h)
    dst = trans.generate()

    return dst

# def distort(src, segment):
#     img_h, img_w = src.shape[:2]
#     dst = np.zeros_like(src, dtype=np.uint8)
#
#     cut = img_w // segment
#     thresh = img_h // 8
#
#     src_pts = list()
#     # dst_pts = list()
#
#     src_pts.append([-np.random.randint(thresh), -np.random.randint(thresh)])
#     src_pts.append([-np.random.randint(thresh), img_h + np.random.randint(thresh)])
#
#     # dst_pts.append([0, 0])
#     # dst_pts.append([0, img_h])
#     dst_box = np.array([[0, 0], [0, img_h], [cut, 0], [cut, img_h]], dtype=np.float32)
#
#     half_thresh = thresh * 0.5
#
#     for cut_idx in np.arange(1, segment, 1):
#         src_pts.append([cut * cut_idx + np.random.randint(thresh) - half_thresh,
#                         np.random.randint(thresh) - half_thresh])
#         src_pts.append([cut * cut_idx + np.random.randint(thresh) - half_thresh,
#                         img_h + np.random.randint(thresh) - half_thresh])
#
#         # dst_pts.append([cut * i, 0])
#         # dst_pts.append([cut * i, img_h])
#
#         src_box = np.array(src_pts[-4:-2] + src_pts[-2:-1] + src_pts[-1:], dtype=np.float32)
#
#         # mat = cv2.getPerspectiveTransform(src_box, dst_box)
#         # print(mat)
#         # dst[:, cut * (cut_idx - 1):cut * cut_idx] = cv2.warpPerspective(src, mat, (cut, img_h))
#
#         mat = get_perspective_transform(dst_box, src_box)
#         dst[:, cut * (cut_idx - 1):cut * cut_idx] = warp_perspective(src, mat, (cut, img_h))
#         # print(mat)
#
#     src_pts.append([img_w + np.random.randint(thresh) - half_thresh,
#                     np.random.randint(thresh) - half_thresh])
#     src_pts.append([img_w + np.random.randint(thresh) - half_thresh,
#                     img_h + np.random.randint(thresh) - half_thresh])
#     src_box = np.array(src_pts[-4:-2] + src_pts[-2:-1] + src_pts[-1:], dtype=np.float32)
#
#     # mat = cv2.getPerspectiveTransform(src_box, dst_box)
#     # dst[:, cut * (segment - 1):] = cv2.warpPerspective(src, mat, (img_w - cut * (segment - 1), img_h))
#     mat = get_perspective_transform(dst_box, src_box)
#     dst[:, cut * (segment - 1):] = warp_perspective(src, mat, (img_w - cut * (segment - 1), img_h))
#
#     return dst