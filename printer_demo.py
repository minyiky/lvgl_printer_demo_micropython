##### startup script #####

import imp, sys
sys.path.append('https://raw.githubusercontent.com/littlevgl/lv_binding_micropython/master/lib')
import display_driver
import lvgl as lv
lv.init()

##### main script #####

##### DEFINES #####
LV_VER_RES = 240
LV_HOR_RES = 320

## Bg positions ##
LV_DEMO_PRINTER_BG_NONE = -LV_VER_RES
LV_DEMO_PRINTER_BG_FULL = 0
LV_DEMO_PRINTER_BG_NORMAL = -2 * (LV_VER_RES / 3)
LV_DEMO_PRINTER_BG_SMALL = -5 * (LV_VER_RES / 6)

## Sizes ##
LV_DEMO_PRINTER_BTN_H = 50
LV_DEMO_PRINTER_BTN_W = 200

## Animations ##
LV_DEMO_PRINTER_ANIM_Y = lv.VER_RES / 20
LV_DEMO_PRINTER_ANIM_DELAY = 40
LV_DEMO_PRINTER_ANIM_TIME = 150
LV_DEMO_PRINTER_ANIM_TIME_BG = 300

## Padding ##
LV_DEMO_PRINTER_TITLE_PAD = 35


##### CALLBACKS ######
def copy_open_icon_event_cb(s, e):
    if e == lv.EVENT.CLICKED:
        scan_btn_txt = "NEXT"
        lv_demo_printer_anim_out_all(scr, 0)
        uint32_t delay = 200
        lv_demo_printer_anim_bg(150, LV_DEMO_PRINTER_BLUE, LV_DEMO_PRINTER_BG_FULL)

        arc = add_loader(scr, scan_anim_ready)
        arc.align(arc.get_parent(), lv.ALIGN.CENTER, 0, -40)

        txt = lv.label(scr)
        txt.set_text("Scanning, please wait...")
        lv.theme_apply(txt, LV_DEMO_PRINTER_THEME_LABEL_WHITE)
        txt.align(arc, lv.ALIGN.OUT_BOTTOM_MID, 0, 60)

        lv_demo_printer_anim_in(arc, delay)
        delay += LV_DEMO_PRINTER_ANIM_DELAY
        lv_demo_printer_anim_in(txt, delay)

    icon_generic_event_cb(s, e)


def scan_open_icon_event_cb(s, e):
    if e == lv.EVENT.CLICKED:
        scan_btn_txt = "SAVE"
        lv_demo_printer_anim_out_all(scr, 0)
        uint32_t delay = 200
        lv_demo_printer_anim_bg(150, LV_DEMO_PRINTER_BLUE, LV_DEMO_PRINTER_BG_FULL)

        arc = add_loader(scr, scan_anim_ready)
        arc.align(arc.get_parent, lv.ALIGN.CENTER, 0, -40)

        txt = lv.label(scr)
        txt.set_text("Scanning, please wait...")
        lv.theme_apply(txt, LV_DEMO_PRINTER_THEME_LABEL_WHITE)
        txt.align(arc, lv.ALIGN.OUT_BOTTOM_MID, 0, 60)

        lv_demo_printer_anim_in(arc, delay)
        delay += LV_DEMO_PRINTER_ANIM_DELAY
        lv_demo_printer_anim_in(txt, delay)


def scan_save_event_cb(s, e):
    if e == lv.EVENT.CLICKED:
        scan_img = NULL

        lv_demo_printer_anim_out_all(scr, 0)
        lv_demo_printer_anim_bg(0, LV_DEMO_PRINTER_GREEN, LV_DEMO_PRINTER_BG_FULL)

        uint32_t delay = 200

        LV_IMG_DECLARE(lv_demo_printer_img_ready)
        img = lv.img(scr)
        img.set_src(img, &lv_demo_printer_img_ready)
        img.align(img.get_parent, lv.ALIGN.CENTER, 0, -40)

        delay += LV_DEMO_PRINTER_ANIM_DELAY
        lv_demo_printer_anim_in(img, delay)

        info_bottom("File saved", "CONTINUE", back_to_home_event_cb, delay)


def usb_icon_event_cb(s, e):
    if e == lv.EVENT.CLICKED:
        lv_demo_printer_anim_out_all(scr, 0)

        uint32_t delay = 200

        back = add_back(scr, back_to_print_event_cb)
        lv_demo_printer_anim_in(back, delay)

        title = add_title(scr, "PRINTING FROM USB DRIVE")
        lv_demo_printer_anim_in(title, delay)

        box_w = (LV_HOR_RES * 5) // 10
        list = lv.list(scr)
        list.set_size(box_w, LV_VER_RES // 2)
        list.align(list.get_parent(), lv.ALIGN.IN_TOP_LEFT, LV_HOR_RES // 20, LV_VER_RES // 5)

        dummy_file_list = [ "Contract 12.pdf", "Scanned_05_21.pdf", "Photo_132210.jpg", "Photo_232141.jpg",
                 "Photo_091640.jpg", "Photo_124019.jpg", "Photo_232032.jpg", "Photo_232033.jpg", "Photo_232034.jpg",
                 "Monday schedule.pdf", "Email from John.txt", "New file.txt", "Untitled.txt", "Untitled (1).txt", "Gallery_40.jpg",
                 "Gallery_41.jpg", "Gallery_42.jpg", "Gallery_43.jpg", "Gallery_44.jpg" ]


        for i in range(0, len(dummy_file_list)):
             btn = list.add_btn(lv.SYMBOL.FILE, dummy_file_list[i])
             btn.set_checkable(True)

        dropdown_box = lv.obj(scr)
        dropdown_box.set_size(box_w, LV_VER_RES // 5)
        dropdown_box.align(list, lv.ALIGN.OUT_BOTTOM_MID, 0, LV_HOR_RES // 30)

        dropdown = lv.dropdown(dropdown_box)
        dropdown.align(dropdown.get_parent(), lv.ALIGN.IN_LEFT_MID, LV_HOR_RES // 60, 0)
        dropdown.set_max_height(LV_VER_RES // 3)
        dropdown.set_options_static("Best\nNormal\nDraft")
        dropdown.set_width((box_w - 3 * LV_HOR_RES // 60) // 2)
        dropdown.set_ext_click_area(5, 5, 5, 5)

        dropdown = lv.dropdown(dropdown_box, dropdown)
        dropdown.align(dropdown.get_parent(), lv.ALIGN.IN_RIGHT_MID, - LV_HOR_RES // 60, 0)
        dropdown.set_options_static("100 DPI\n200 DPI\n300 DPI\n400 DPI\n500 DPI\n1500 DPI")

        box_w = 320 - 40
        settings_box = lv.obj(scr)
        settings_box.set_size(box_w, LV_VER_RES // 2)
        settings_box.align(list, lv.ALIGN.OUT_RIGHT_TOP, LV_HOR_RES // 20, 0)

        print_cnt = 1
        numbox = lv.cont(settings_box)
        lv.theme_apply(numbox, LV_DEMO_PRINTER_THEME_BOX_BORDER)
        numbox.set_size(LV_HOR_RES // 7, LV_HOR_RES // 13)
        numbox.align(settings_box, lv.ALIGN.IN_TOP_MID, 0, LV_VER_RES // 10)
        numbox.set_style_local_value_str(numbox.PART.MAIN, lv.STATE.DEFAULT, "Copies")
        numbox.set_style_local_value_align(numbox.PART.MAIN, lv.STATE.DEFAULT, lv.ALIGN.OUT_TOP_MID)
        numbox.set_style_local_value_ofs_y(numbox.PART.MAIN, lv.STATE.DEFAULT, - LV_VER_RES // 50)
        numbox.set_style_local_value_font(numbox.PART.MAIN, lv.STATE.DEFAULT, lv.theme_get_font_subtitle())
        numbox.set_layout(lv.LAYOUT.CENTER)

        print_cnt_label = lv.label(numbox)
        print_cnt_label.set_text("1")
        print_cnt_label.set_style_local_text_font(lv.label_PART.MAIN, lv.STATE.DEFAULT, lv.theme_get_font_title())

        btn = lv.btn(settings_box)
        btn.set_size(LV_HOR_RES // 13, LV_HOR_RES // 13)
        btn.align(numbox, lv.ALIGN.OUT_LEFT_MID, - LV_VER_RES // 60, 0)
        btn.set_style_local_value_str(btn.PART.MAIN, lv.STATE.DEFAULT, lv.SYMBOL.DOWN)
        btn.set_event_cb(print_cnt_bnt_event_cb)
        btn.set_ext_click_area(10, 10, 10, 10)

        sw = lv.switch(settings_box)
        sw.set_size(sw, LV_HOR_RES // 10, LV_VER_RES // 12)
        sw.align(btn, lv.ALIGN.OUT_BOTTOM_LEFT, LV_HOR_RES // 50, LV_VER_RES // 7)
        sw.set_style_local_value_ofs_y(sw.PART.MAIN, lv.STATE.DEFAULT, - LV_VER_RES // 50)
        sw.set_style_local_value_align(sw.PART.MAIN, lv.STATE.DEFAULT, lv.ALIGN.OUT_TOP_MID)
        sw.set_style_local_value_str(sw.PART.MAIN, lv.STATE.DEFAULT, "Color")
        sw.set_style_local_value_font(sw.PART.MAIN, lv.STATE.DEFAULT, lv.theme_get_font_subtitle())

        btn = lv.btn(settings_box, btn)
        btn.align(numbox, lv.ALIGN.OUT_RIGHT_MID, LV_VER_RES // 60, 0)
        btn.set_style_local_value_str(btn.PART.MAIN, lv.STATE.DEFAULT, lv.SYMBOL.UP)

        sw = lv.switch(settings_box, sw)
        sw.align(btn, lv.ALIGN.OUT_BOTTOM_RIGHT, - LV_HOR_RES // 50, LV_VER_RES // 7)
        sw.set_style_local_value_str(sw.PART.MAIN, lv.STATE.DEFAULT, "Vertical")

        print_btn = lv.btn(scr)
        lv.theme_apply(print_btn, LV_DEMO_PRINTER_THEME_BTN_CIRCLE)
        print_btn.set_size(box_w, 60)

        btn_ofs_y = (dropdown_box.get_height() - print_btn.get_height()) // 2
        print_btn.align(settings_box, lv.ALIGN.OUT_BOTTOM_MID, 0, LV_HOR_RES // 30 + btn_ofs_y)
        print_btn.set_style_local_value_str(print_btn.PART.MAIN, lv.STATE.DEFAULT, "PRINT")
        print_btn.set_style_local_value_font(print_btn.PART.MAIN, lv.STATE.DEFAULT, lv.theme_get_font_subtitle())
        print_btn.set_style_local_bg_color(print_btn.PART.MAIN, lv.STATE.DEFAULT, LV_DEMO_PRINTER_GREEN)
        print_btn.set_style_local_bg_color(print_btn.PART.MAIN, lv.STATE.PRESSED, lv_color_darken(LV_DEMO_PRINTER_GREEN, LV_OPA_20))
        print_btn.set_event_cb(print_start_event_cb)

        delay += LV_DEMO_PRINTER_ANIM_DELAY
        lv_demo_printer_anim_in(list, delay)

        delay += LV_DEMO_PRINTER_ANIM_DELAY
        lv_demo_printer_anim_in(settings_box, delay)

        delay += LV_DEMO_PRINTER_ANIM_DELAY
        lv_demo_printer_anim_in(dropdown_box, delay)

        delay += LV_DEMO_PRINTER_ANIM_DELAY
        lv_demo_printer_anim_in(print_btn, delay)

        lv_demo_printer_anim_bg(0, LV_DEMO_PRINTER_BLUE, LV_DEMO_PRINTER_BG_NORMAL)


def print_cnt_bnt_event_cb(s, e):
    if e == lv.EVENT.CLICKED or e == lv.EVENT.LONG_PRESSED_REPEAT:
        txt = s.get_style_value_str(s.PART.MAIN)
        if txt == lv.SYMBOL.DOWN:
            if print_cnt > 1:
                print_cnt -= 1
        else:
            if print_cnt < 1000:
                print_cnt += 1

        print_cnt_label.set_text_fmt(print_cnt_label, str(print_cnt))


def print_start_event_cb(s, e):
    if e == lv.EVENT.CLICKED:
        lv_demo_printer_anim_out_all(scr, 0)
        delay = 200
        lv_demo_printer_anim_bg(150, LV_DEMO_PRINTER_BLUE, LV_DEMO_PRINTER_BG_FULL)

        arc = add_loader(scr, print_start_ready)
        arc.align(arc.get_parent(), lv.ALIGN.CENTER, 0, -40)

        txt = lv.label(scr)
        txt.set_text("Printing, please wait...")
        lv.theme_apply(txt, LV_DEMO_PRINTER_THEME_LABEL_WHITE)
        txt.align(arc, lv.ALIGN.OUT_BOTTOM_MID, 0, 60)

        lv_demo_printer_anim_in(arc, delay)
        delay += LV_DEMO_PRINTER_ANIM_DELAY
        lv_demo_printer_anim_in(txt, delay)


def back_to_print_event_cb(s, e):
    if e == lv.EVENT.CLICKED:
        lv_demo_printer_anim_out_all(scr, 0)
        print_open(150)


def mobile_icon_event_cb(s, e):
    if e == lv.EVENT.CLICKED:
        lv_demo_printer_anim_out_all(scr, 0)

        lv_demo_printer_anim_bg(0, LV_DEMO_PRINTER_BLUE, LV_DEMO_PRINTER_BG_FULL)

        delay = 200

        LV_IMG_DECLARE(lv_demo_printer_img_printer2)

        img = lv_img(scr)
        img.set_src(&lv_demo_printer_img_printer2)
        img.align(img.get_parent(), lv.ALIGN.CENTER, -90, 0)

        lv_demo_printer_anim_in(img, delay)
        delay += LV_DEMO_PRINTER_ANIM_DELAY

        LV_IMG_DECLARE(lv_demo_printer_img_wave)
        img = lv_img(scr)
        img.set_src(&lv_demo_printer_img_wave)
        img.align(img.get_parent(), lv.ALIGN.CENTER, 0, 0)

        lv_demo_printer_anim_in(img, delay)
        delay += LV_DEMO_PRINTER_ANIM_DELAY

        LV_IMG_DECLARE(lv_demo_printer_img_phone)
        img = lv_img(scr)
        img.set_src(&lv_demo_printer_img_phone)
        img.align(img.get_parent(), lv.ALIGN.CENTER, 80, 0)

        lv_demo_printer_anim_in(img, delay)
        delay += LV_DEMO_PRINTER_ANIM_DELAY

        info_bottom("Put you phone near to the printer", "BACK", back_to_print_event_cb, delay)

    icon_generic_event_cb(s, e)


def internet_icon_event_cb(s, e):
    if e == lv.EVENT.CLICKED:
        lv_demo_printer_anim_out_all(scr, 0)

        lv_demo_printer_anim_bg(0, LV_DEMO_PRINTER_RED, LV_DEMO_PRINTER_BG_FULL)

        uint32_t delay = 200

        LV_IMG_DECLARE(lv_demo_printer_img_printer2)

        t * img = lv_img(scr)
        lv_img_set_src(img, &lv_demo_printer_img_printer2)
        align(img, lv.ALIGN.CENTER, -90, 0)

        lv_demo_printer_anim_in(img, delay)
        delay += LV_DEMO_PRINTER_ANIM_DELAY

        LV_IMG_DECLARE(lv_demo_printer_img_no_internet)
        img = lv_img(scr)
        lv_img_set_src(img, &lv_demo_printer_img_no_internet)
        align(img, lv.ALIGN.CENTER, 0, -40)

        lv_demo_printer_anim_in(img, delay)
        delay += LV_DEMO_PRINTER_ANIM_DELAY

        LV_IMG_DECLARE(lv_demo_printer_img_cloud)
        img = lv_img(scr)
        lv_img_set_src(img, &lv_demo_printer_img_cloud)
        align(img, lv.ALIGN.CENTER, 80, -80)

        lv_demo_printer_anim_in(img, delay)
        delay += LV_DEMO_PRINTER_ANIM_DELAY

        info_bottom("No internet connection", "BACK", back_to_print_event_cb, delay)
    }

    icon_generic_event_cb(obj, e)


def setup_icon_event_cb(s, e):
    if e == lv.EVENT.CLICKED:
        lv_demo_printer_anim_out_all(scr, 0)

        lv_demo_printer_anim_bg(0, LV_DEMO_PRINTER_RED, LV_DEMO_PRINTER_BG_FULL)

        delay = 200

        LV_IMG_DECLARE(lv_demo_printer_img_printer2)

        img = lv_img(scr)
        img.set_src(&lv_demo_printer_img_printer2)
        img.align(img.get_parent, lv.ALIGN.CENTER, -90, 0)

        lv_demo_printer_anim_in(img, delay)
        delay += LV_DEMO_PRINTER_ANIM_DELAY

        LV_IMG_DECLARE(lv_demo_printer_img_no_internet)
        img = lv_img(scr)
        img.set_src(&lv_demo_printer_img_no_internet)
        img.align(img.get_parent(), lv.ALIGN.CENTER, 0, -40)

        lv_demo_printer_anim_in(img, delay)
        delay += LV_DEMO_PRINTER_ANIM_DELAY

        LV_IMG_DECLARE(lv_demo_printer_img_cloud)
        img = lv_img(scr)
        img.set_src(&lv_demo_printer_img_cloud)
        img.align(img.get_parent(), lv.ALIGN.CENTER, 80, -80)

        lv_demo_printer_anim_in(img, delay)
        delay += LV_DEMO_PRINTER_ANIM_DELAY

        info_bottom("You have no permission to change the settings.", "BACK", back_to_home_event_cb, delay)

    icon_generic_event_cb(s, e)


def print_open_event_cb(s, e):
    if e == lv.EVENT.CLICKED:
        lv_demo_printer_anim_out_all(scr, 0)
        print_open(200)
    icon_generic_event_cb(s, e)


def back_to_home_event_cb(s, e):
    if e == lv.EVENT.CLICKED:
        scan_img = None
        lv_demo_printer_anim_out_all(scr, 0)
        home_open(200)


def scan_next_event_cb(s, e):
    if e == lv.EVENT.CLICKED:
        lv_demo_printer_anim_out_all(scr, 0)

        delay = 400

        back = add_back(back_to_home_event_cb)
        lv_demo_printer_anim_in(back, delay)

        title = add_title("ADJUST IMAGE")
        lv_demo_printer_anim_in(title, delay)

        box_w = 400
        scan_img.set_pivot(0, 0)
        scan_imgset_antialias(False)
        a = a.t()
        a.init()
        a.set_var(scan_img)
        a.set_exec_cb(lv_img_set_zoom)
        a.set_values(LV_IMG_ZOOM_NONE, 190)
        a.set_time(200)
        a.set_delay(200)
        a.start()
        scan_img = None

        dropdown_box = lv.obj(scr)
        dropdown_box.set_size(box_w, LV_VER_RES // 5)
        dropdown_box.align(dropdown_box.get_parent(), lv.ALIGN.IN_BOTTOM_LEFT, 40, -20)

        dropdown = lv_dropdown(dropdown_box)
        dropdown.align(dropdown.get_parent(), lv.ALIGN.IN_LEFT_MID, LV_HOR_RES // 60, 0)
        dropdown.set_max_height(LV_VER_RES // 3)
        dropdown.set_options_static("Best\nNormal\nDraft")
        dropdown.set_width((box_w - 3 * LV_HOR_RES // 60) // 2)

        dropdown = lv_dropdown(dropdown_box, dropdown)
        dropdown.align(dropdown.get_parent(), lv.ALIGN.IN_RIGHT_MID, - LV_HOR_RES // 60, 0)
        dropdown.set_options_static("72 DPI\n96 DPI\n150 DPI\n300 DPI\n600 DPI\n900 DPI\n1200 DPI")

        box_w = 320 - 40
        settings_box = lv.obj(scr)
        settings_box.set_size(box_w, LV_VER_RES // 2)
        settings_box.align(settings_box.get_parent(), lv.ALIGN.IN_TOP_RIGHT, -40, 100)

        numbox = lv.cont(settings_box)
        lv.theme_apply(numbox, LV_DEMO_PRINTER_THEME_BOX_BORDER)
        numbox.set_size(numbox, LV_HOR_RES // 7, LV_HOR_RES // 13)
        numbox.align(settings_box, lv.ALIGN.IN_TOP_MID, 0, LV_VER_RES // 10)
        numbox.set_style_local_value_str(numbox.PART.MAIN, lv.STATE.DEFAULT, "Copies")
        numbox.set_style_local_value_align(numbox.PART.MAIN, lv.STATE.DEFAULT, lv.ALIGN.OUT_TOP_MID)
        numbox.set_style_local_value_ofs_y(numbox.PART.MAIN, lv.STATE.DEFAULT, - LV_VER_RES // 50)
        numbox.set_style_local_value_font(numbox.PART.MAIN, lv.STATE.DEFAULT, lv.theme_get_font_subtitle())
        numbox.set_layout(lv.LAYOUT.CENTER)

        print_cnt = 1
        print_cnt_label = lv.label(numbox)
        print_cnt_label.set_text(, "1")
        print_cnt_label.set_style_local_text_font(print_cnt_label.PART.MAIN, lv.STATE.DEFAULT, lv.theme_get_font_title())

        btn = lv.btn(settings_box)
        btn.set_size(LV_HOR_RES // 13, LV_HOR_RES // 13)
        btn.align(numbox, lv.ALIGN.OUT_LEFT_MID, - LV_VER_RES // 60, 0)
        btn.set_style_local_value_str(btn.PART.MAIN, lv.STATE.DEFAULT, lv.SYMBOL.DOWN)
        btn.set_event_cb(print_cnt_bnt_event_cb)
        btn.set_ext_click_area(10, 10, 10, 10)

        sw = lv.switch(settings_box)
        sw.set_size(LV_HOR_RES // 10, LV_VER_RES // 12)
        sw.align(btn, lv.ALIGN.OUT_BOTTOM_LEFT, LV_HOR_RES // 50, LV_VER_RES // 7)
        sw.set_style_local_value_ofs_y(sw.PART.MAIN, lv.STATE.DEFAULT, - LV_VER_RES // 50)
        sw.set_style_local_value_align(sw.PART.MAIN, lv.STATE.DEFAULT, lv.ALIGN.OUT_TOP_MID)
        sw.set_style_local_value_str(sw.PART.MAIN, lv.STATE.DEFAULT, "Color")
        sw.set_style_local_value_font(sw.PART.MAIN, lv.STATE.DEFAULT, lv.theme_get_font_subtitle())

        btn = lv.btn(settings_box, btn)
        btn.align(btn, numbox, lv.ALIGN.OUT_RIGHT_MID, LV_VER_RES / 60, 0)
        btn.set_style_local_value_str(btn.PART.MAIN, lv.STATE.DEFAULT, lv.SYMBOL.UP)

        sw = lv.switch(settings_box, sw)
        sw.align(btn, lv.ALIGN.OUT_BOTTOM_RIGHT, - LV_HOR_RES / 50, LV_VER_RES / 7)
        sw.set_style_local_value_str(sw.PART.MAIN, lv.STATE.DEFAULT, "Vertical")

        print_btn = lv.btn(scr)
        lv.theme_apply(print_btn, LV_DEMO_PRINTER_THEME_BTN_CIRCLE)
        print_btn.set_size(box_w, 60)
        print_btn.set_event_cb(print_start_event_cb)

        btn_ofs_y = (dropdown_box.get_height() - print_btn.get_height()) // 2
        print_btn.align(print_btn, settings_box, lv.ALIGN.OUT_BOTTOM_MID, 0, LV_HOR_RES // 30 + btn_ofs_y)
        print_btn.set_style_local_value_str(print_btn.PART.MAIN, lv.STATE.DEFAULT, "PRINT")
        print_btn.set_style_local_value_font(print_btn.PART.MAIN, lv.STATE.DEFAULT, lv.theme_get_font_subtitle())
        print_btn.set_style_local_bg_color(print_btn.PART.MAIN, lv.STATE.DEFAULT, LV_DEMO_PRINTER_GREEN)
        print_btn.set_style_local_bg_color(print_btn.PART.MAIN, lv.STATE.PRESSED, lv_color_darken(LV_DEMO_PRINTER_GREEN, LV_OPA_20))

        delay += LV_DEMO_PRINTER_ANIM_DELAY
        lv_demo_printer_anim_in(settings_box, delay)

        delay += LV_DEMO_PRINTER_ANIM_DELAY
        lv_demo_printer_anim_in(dropdown_box, delay)

        delay += LV_DEMO_PRINTER_ANIM_DELAY
        lv_demo_printer_anim_in(print_btn, delay)

        lv_demo_printer_anim_bg(0, LV_DEMO_PRINTER_BLUE, LV_DEMO_PRINTER_BG_NORMAL)


def hue_slider_event_cb(s, e):
    if e == lv.EVENT.VALUE_CHANGED:
        hue_act = lv_slider_get_value(s)
        scan_img_color_refr()


def lightness_slider_event_cb(s, e):
    if e == lv.EVENT.VALUE_CHANGED:
        lightness_act = lv_slider_get_value(s)
        scan_img_color_refr()


def icon_generic_event_cb(s, e):
    if e == lv.EVENT.PRESSED:
        img = s.get_child_back()
        txt = s.get_child()

        a = lv.anim_t()
        a.init()
        a.set_time(100)

        a.set_var(img)
        a.set_exec_cb(set_x)
        a.set_values(img.get_x(), s.get_width() - img.get_width() - 35)
        a.start()

        a.set_exec_cb(set_y)
        a.set_values(img.get_y())
        a.start()

        a.set_var(txt)
        a.set_exec_cb(set_x)
        a.set_values(txt.get_x(), 35)
        a.start()

        a.set_exec_cb(set_y)
        a.set_values(txt.get_y(), s.get_height() - txt.get_height() - 35)
        a.start()

    elif e == lv.EVENT.PRESS_LOST or e == lv.EVENT.RELEASED:
        img = s.get_child_back()
        txt = s.get_child()
        a = lv.anim_t()
        a.init()
        a.set_time(100)
        a.set_var(img)

        a.set_exec_cb(set_x)
        a.set_values(img.get_x(), s.get_width() - img.get_width() - 30)
        a.start()

        a.set_exec_cb(set_y)
        a.set_values(img.get_y(), 30)
        a.start()

        a.set_var(txt)
        a.set_exec_cb(set_x)
        a.set_values(txt.get_x(), 30)
        a.start()

        a.set_exec_cb(set_y)
        a.set_values(txt.get_y(), s.get_height(obj) - txt.get_height() - 30)
        a.start()


##### STATIC FUNCTIONS #####

def home_open(parent, delay):
    # TODO
    DECLARE(lv_demo_printer_icon_wifi)
    DECLARE(lv_demo_printer_icon_tel)
    DECLARE(lv_demo_printer_icon_eco)
    DECLARE(lv_demo_printer_icon_pc)


    cont = lv.cont(parent)
    cont.set_size(350, 80)
    cont.clean_style_list(cont.PART.MAIN)
    cont.align(parent, lv.ALIGN.IN_TOP_LEFT, 60, 0)

    icon = lv.img(cont)
    icon.set_src(icon, &lv_demo_printer_icon_wifi)
    icon.align(cont, lv.ALIGN.IN_TOP_LEFT, 20, 50)
    lv_demo_printer_anim_in(icon, delay) # TODO:

    icon = lv.img(cont)
    icon.set_scr(&lv_demo_printer_icon_tel)
    icon.align(, lv.ALIGN.IN_TOP_LEFT, 110, 50)
    lv_demo_printer_anim_in(icon, delay) # TODO:

    icon = lv.img(cont)
    icon.set_scr(&lv_demo_printer_icon_eco)
    icon.align(, lv.ALIGN.IN_TOP_LEFT, 200, 50)
    lv_demo_printer_anim_in(icon, delay) # TODO:

    icon = lv.img(cont)
    icon.set_scr(&lv_demo_printer_icon_pc)
    icon.align(, lv.ALIGN.IN_TOP_LEFT, 290, 50)
    lv_demo_printer_anim_in(icon, delay) # TODO:

    title = add_title("22 April 2020 15:36") # TODO:
    title.align(parent, lv.ALIGN.IN_TOP_RIGHT, -60, LV_DEMO_PRINTER_TITLE_PAD)

    delay += LV_DEMO_PRINTER_ANIM_DELAY
    lv_demo_printer_anim_in(title, delay) # TODO:

    box_w = 720
    box = lv.box(parent)
    box.set_size(box_w, 260)
    box.align(parent, lv.ALIGN.IN_TOP_MID, 0, 100)
    delay += LV_DEMO_PRINTER_ANIM_DELAY
    lv_demo_printer_anim_in(box, delay) # TODO:

    # TODO: Impliment DECLARE
    DECLARE(lv_demo_printer_img_btn_bg_1)
    DECLARE(lv_demo_printer_img_btn_bg_2)
    DECLARE(lv_demo_printer_img_btn_bg_3)
    DECLARE(lv_demo_printer_img_btn_bg_4)

    DECLARE(lv_demo_printer_img_copy)
    DECLARE(lv_demo_printer_img_scan)
    DECLARE(lv_demo_printer_img_print)
    DECLARE(lv_demo_printer_img_setup)

    icon = add_icon(box, &lv_demo_printer_img_btn_bg_1, &lv_demo_printer_img_copy, "COPY") # TODO:
    icon.align(box, lv.ALIGN.IN_LEFT_MID, 1 * (box_w - 20) // 8 + 10, 0)
    set_event_cb(icon, copy_open_icon_event_cb) # TODO:
    fade_in(icon, LV_DEMO_PRINTER_ANIM_TIME * 2, delay + LV_DEMO_PRINTER_ANIM_TIME + 50) # TODO:

    icon = add_icon(box, &lv_demo_printer_img_btn_bg_2, &lv_demo_printer_img_scan, "SCAN") # TODO:
    icon.align(box, lv.ALIGN.IN_LEFT_MID, 3 * (box_w - 20) // 8 + 10, 0)
    fade_in(icon, LV_DEMO_PRINTER_ANIM_TIME * 2, delay + LV_DEMO_PRINTER_ANIM_TIME + 50) # TODO:
    set_event_cb(icon, scan_open_icon_event_cb) # TODO:

    icon = add_icon(box, &lv_demo_printer_img_btn_bg_3, &lv_demo_printer_img_print, "PRINT") # TODO:
    icon.align(box, lv.ALIGN.IN_LEFT_MID, 5 * (box_w - 20) // 8 + 10, 0)
    fade_in(icon, LV_DEMO_PRINTER_ANIM_TIME * 2, delay + LV_DEMO_PRINTER_ANIM_TIME + 50) # TODO:
    set_event_cb(icon, print_open_event_cb) # TODO:

    icon = add_icon(box, &lv_demo_printer_img_btn_bg_4, &lv_demo_printer_img_setup, "SETUP") # TODO:
    icon.align(box, lv.ALIGN.IN_LEFT_MID, 7 * (box_w - 20) // 8 + 10, 0)
    fade_in(icon, LV_DEMO_PRINTER_ANIM_TIME * 2, delay + LV_DEMO_PRINTER_ANIM_TIME + 50) # TODO:
    set_event_cb(icon, setup_icon_event_cb) # TODO:

    box = lv.box(parent)
    box.set_size(500, 80)
    box.align(parent, lv.ALIGN.IN_BOTTOM_LEFT, LV_HOR_RES // 20, - LV_HOR_RES // 40)
    box.set_style_local_value_str(box.PART.MAIN, lv.STATE.DEFAULT, "What do you want to do today?")

    delay += LV_DEMO_PRINTER_ANIM_DELAY
    lv_demo_printer_anim_in(box, delay) # TODO:

    box = lv.box(parent)
    box_w = 200
    box.set_size(box_w, 80)
    box.align(parent, lv.ALIGN.IN_BOTTOM_RIGHT, - LV_HOR_RES // 20, - LV_HOR_RES // 40)

    bar = lv.bar(box)
    bar.set_style_local_bg_color(bar.PART.INDIC, lv.STATE.DEFAULT, lv_color_hex(0x01d3d4))
    bar.set_size(25, 50)
    bar.align(box, lv.ALIGN.IN_LEFT_MID, 1 * (box_w - 20) // 8 + 10, 0)
    bar.set_value(60, lv.ANIM.ON)

    bar = lv.bar(box)
    bar.set_style_local_bg_color(bar.PART.INDIC, lv.STATE.DEFAULT, lv_color_hex(0xe600e6))
    bar.set_size(25, 50)
    bar.align(box, lv.ALIGN.IN_LEFT_MID, 3 * (box_w - 20) // 8 + 10, 0)
    bar.set_value(30, lv.ANIM.ON)

    bar = lv.bar(box)
    bar.set_style_local_bg_color(bar.PART.INDIC, lv.STATE.DEFAULT, lv_color_hex(0xefef01))
    bar.set_size(25, 50)
    bar.align(box, lv.ALIGN.IN_LEFT_MID, 5 * (box_w - 20) // 8 + 10, 0)
    bar.set_value(80, lv.ANIM.ON)

    bar = lv.bar(box)
    bar.set_style_local_bg_color(bar.PART.INDIC, lv.STATE.DEFAULT, lv_color_hex(0x1d1d25))
    bar.set_size(25, 50)
    bar.align(box, lv.ALIGN.IN_LEFT_MID, 7 * (box_w - 20) // 8 + 10, 0)
    bar.set_value(20, lv.ANIM.ON)

    delay += LV_DEMO_PRINTER_ANIM_DELAY
    lv_demo_printer_anim_in(box, delay)

    first_run = True
    if first_run:
         first_run = False
    else:
        lv_demo_printer_anim_bg(0, LV_DEMO_PRINTER_BLUE, LV_DEMO_PRINTER_BG_NORMAL) # TODO:


def scan1_open(btn_txt, parent):
    lv_demo_printer_anim_out_all(scr, 0) # TODO:

    lv_demo_printer_anim_bg(0, LV_DEMO_PRINTER_BLUE, LV_DEMO_PRINTER_BG_NORMAL) # TODO:

    delay = 200

    back = add_back(back_to_home_event_cb) # TODO:
    lv_demo_printer_anim_in(back, delay) # TODO:

    title = add_title("ADJUST IMAGE") # TODO:
    lv_demo_printer_anim_in(title, delay) # TODO:
    delay += LV_DEMO_PRINTER_ANIM_DELAY

    DECLARE(lv_demo_printer_img_scan_example) # TODO:
    scan_img = lv.img(parent)
    scan_img.set_src(&lv_demo_printer_img_scan_example)
    scan_img.align(parent, lv.ALIGN.IN_TOP_LEFT, 40, 100)
    scan_img.set_style_local_radius(scan_img.PART.MAIN, lv.STATE.DEFAULT, 10)
    scan_img.set_style_local_clip_corner(scan_img.PART.MAIN, lv.STATE.DEFAULT, True)
    scan_img.set_style_local_image_recolor_opa(scan_img.PART.MAIN, lv.STATE.DEFAULT, 80)

    box_w = 160
    settings_box = lv.obj(parent)
    settings_box.set_size(settings_box, box_w, 245)
    settings_box.align(settings_box, scan_img, lv.ALIGN.OUT_RIGHT_TOP, 40, 0)

    lightness_act = 0
    hue_act = 180
    DECLARE(lv_demo_printer_icon_bright) # TODO:
    DECLARE(lv_demo_printer_icon_hue) # TODO:

    slider = lv.slider(settings_box)
    slider.set_size(slider, 8, 160)
    slider.align(settings_box, lv.ALIGN.IN_TOP_MID, - 35, 65)
    slider.set_event_cb(lightness_slider_event_cb)
    slider.set_range(-80, 80)
    slider.set_value(0, lv.ANIM.OFF)
    slider.set_ext_click_area(slider, 30, 30, 30, 30)

    icon = lv.img(settings_box)
    icon.set_src(&lv_demo_printer_icon_bright)
    icon.align(slider, lv.ALIGN.OUT_TOP_MID, 0, -30)

    slider = lv.slider(settings_box, slider)
    slider.align(settings_box, lv.ALIGN.IN_TOP_MID, 35, 65)
    slider.set_event_cb(hue_slider_event_cb)
    slider.set_range(0, 359)
    slider.set_value(180, lv.ANIM.OFF)

    icon = lv.img(settings_box)
    icon.set_src(&lv_demo_printer_icon_hue)
    icon.align(slider, lv.ALIGN.OUT_TOP_MID, 0, -30)

    scan_img_color_refr() # TODO:

    next_btn = lv.btn(parent)
    next_btn.lv.theme_apply(LV_DEMO_PRINTER_THEME_BTN_CIRCLE) # TODO:
    next_btn.set_size(box_w, 60)
    next_btn.align(scan_img, lv.ALIGN.OUT_RIGHT_BOTTOM, 40, 0)

    if btn_txt == "NEXT":
        next_btn.set_event_cb(scan_next_event_cb)
        next_btn.set_style_local_value_str(PART.MAIN, lv.STATE.DEFAULT, "NEXT")
        next_btn.set_style_local_value_font(PART.MAIN, lv.STATE.DEFAULT, lv.theme_get_font_subtitle())
    elif btn_txt == "SAVE":
        next_btn.set_event_cb(scan_save_event_cb)
        next_btn.set_style_local_value_str(PART.MAIN, lv.STATE.DEFAULT, "SAVE")
        next_btn.set_style_local_value_font(PART.MAIN, lv.STATE.DEFAULT, lv.theme_get_font_subtitle())
        next_btn.set_style_local_bg_color(PART.MAIN, lv.STATE.DEFAULT, LV_DEMO_PRINTER_GREEN)
        next_btn.set_style_local_bg_color(PART.MAIN, lv.STATE.PRESSED, lv_color_darken(LV_DEMO_PRINTER_GREEN, LV_OPA_20))

    lv_demo_printer_anim_in(scan_img, delay) # TODO:
    delay += LV_DEMO_PRINTER_ANIM_DELAY

    lv_demo_printer_anim_in(settings_box, delay) # TODO:
    delay += LV_DEMO_PRINTER_ANIM_DELAY

    lv_demo_printer_anim_in(delay) # TODO:
    delay += LV_DEMO_PRINTER_ANIM_DELAY


def scan_anim_ready(a):
    lv_demo_printer_anim_out_all(lv.scr(), 0)
    scan1_open(scan_btn_txt)


def print_open(delay, parent):
    back = add_back(back_to_home_event_cb) # TODO:
    lv_demo_printer_anim_in(back, delay) # TODO:

    title = add_title("PRINT MENU") # TODO:
    lv_demo_printer_anim_in(title, delay) # TODO:

    box_w = 720
    box = create(parent)
    box.set_size(box_w, 260)
    box.align(parent, lv.ALIGN.IN_TOP_MID, 0, 100)

    delay += LV_DEMO_PRINTER_ANIM_DELAY
    lv_demo_printer_anim_in(box, delay) # TODO:

    # TODO:
    LV_IMG_DECLARE(lv_demo_printer_img_usb)
    LV_IMG_DECLARE(lv_demo_printer_img_mobile)
    LV_IMG_DECLARE(lv_demo_printer_img_internet)
    LV_IMG_DECLARE(lv_demo_printer_img_btn_bg_2)
    LV_IMG_DECLARE(lv_demo_printer_img_btn_bg_3)
    LV_IMG_DECLARE(lv_demo_printer_img_btn_bg_4)

    icon = add_icon(box, &lv_demo_printer_img_btn_bg_2, &lv_demo_printer_img_usb, "USB") # TODO:
    icon.align(icon.get_parent(), lv.ALIGN.IN_LEFT_MID, 1 * box_w // 6, -15)
    icon.set_event_cb(usb_icon_event_cb)
    fade_in(icon, LV_DEMO_PRINTER_ANIM_TIME * 2, delay + LV_DEMO_PRINTER_ANIM_TIME + 50) # TODO:

    icon = add_icon(box, &lv_demo_printer_img_btn_bg_3, &lv_demo_printer_img_mobile, "MOBILE") # TODO:
    icon.align(icon.get_parent(), lv.ALIGN.IN_LEFT_MID, 3 * box_w // 6, -15)
    icon.set_event_cb(mobile_icon_event_cb)
    fade_in(icon, LV_DEMO_PRINTER_ANIM_TIME * 2, delay + LV_DEMO_PRINTER_ANIM_TIME + 50) # TODO:

    icon = add_icon(box, &lv_demo_printer_img_btn_bg_4, &lv_demo_printer_img_internet, "INTERNET") # TODO:
    icon.align(icon.get_parent(), lv.ALIGN.IN_LEFT_MID, 5 * box_w // 6, -15)
    icon.set_event_cb(internet_icon_event_cb)
    fade_in(icon, LV_DEMO_PRINTER_ANIM_TIME * 2, delay + LV_DEMO_PRINTER_ANIM_TIME + 50) # TODO:

    box = lv.obj(parent)
    box.set_size(box, box_w, 80)
    box.align(box.get_parent(), lv.ALIGN.IN_BOTTOM_LEFT, LV_HOR_RES / 20, - LV_HOR_RES / 40)
    box.set_style_local_value_str(box.PART.MAIN, lv.STATE.DEFAULT, "From where do you want to print?")

    delay += LV_DEMO_PRINTER_ANIM_DELAY
    lv_demo_printer_anim_in(box, delay) # TODO:

    lv_demo_printer_anim_bg(0, LV_DEMO_PRINTER_BLUE, LV_DEMO_PRINTER_BG_NORMAL) # TODO:


def print_start_ready(a, parent):
    lv_demo_printer_anim_bg(0, LV_DEMO_PRINTER_GREEN, LV_DEMO_PRINTER_BG_FULL) # TODO:
    lv_demo_printer_anim_out_all(scr, 0) # TODO:

    LV_IMG_DECLARE(lv_demo_printer_img_ready) # TODO:
    img = lv.img(parent)
    img.set_src(&lv_demo_printer_img_ready)
    img.align(img.get_parent(), lv.ALIGN.CENTER, 0, -40)

    delay = 200
    lv_demo_printer_anim_in(img, delay) # TODO:
    delay += LV_DEMO_PRINTER_ANIM_DELAY

    info_bottom("Printing finished", "CONTINUE", back_to_home_event_cb, delay) # TODO:


def info_bottom(dsc, btn_txt, btn_event_cb, delay, parent):
    txt = lv.label(scr)
    txt.set_text(dsc)
    lv.theme_apply(txt, (lv.theme_style_t)LV_DEMO_PRINTER_THEME_LABEL_WHITE) # TODO:
    txt.align(txt.get_parent(), lv.ALIGN.CENTER, 0, 100)

    btn = lv.btn(parent)
    lv.theme_apply(btn, (lv.theme_style_t)LV_DEMO_PRINTER_THEME_BTN_BORDER)
    btn.set_size(LV_DEMO_PRINTER_BTN_W, LV_DEMO_PRINTER_BTN_H)
    btn.align(txt, lv.ALIGN.OUT_BOTTOM_MID, 0, 60)
    btn.set_style_local_value_str(btn.PART.MAIN, lv.STATE.DEFAULT, btn_txt)
    btn.set_event_cb(btn_event_cb)

    lv_demo_printer_anim_in(txt, delay) # TODO:
    delay += LV_DEMO_PRINTER_ANIM_DELAY

    lv_demo_printer_anim_in(btn, delay) # TODO:
    delay += LV_DEMO_PRINTER_ANIM_DELAY

    lv_demo_printer_anim_in(btn, delay) # TODO:


def add_icon(parent, src_bg, src_icon, txt):
    bg = lv.img(parent)
    bg.set_click(True)
    lv.theme_apply(bg, (lv.theme_style_t)LV_DEMO_PRINTER_THEME_ICON) # TODO:
    bg.set_src(src_bg)
    bg.set_antialias(False)

    icon = lv.img(bg)
    icon.set_src(src_icon)
    icon.set_style_local_image_recolor_opa(img.PART.MAIN, lv.STATE.DEFAULT, lv.OPA._0)
    icon.align(parent, lv.ALIGN.IN_TOP_RIGHT, -30, 30)

    label = lv.label(bg)
    label.set_text(txt)
    label.align(parent, lv.ALIGN.IN_BOTTOM_LEFT, 30, -30)

    return bg


def add_title(parent, txt):
    title = lv.label(parent)
    lv.theme_apply(title, (lv.theme_style_t)LV_DEMO_PRINTER_THEME_TITLE) # TODO:
    title.set_text(txt)
    title.align(parent, lv.ALIGN.IN_TOP_MID, 0, LV_DEMO_PRINTER_TITLE_PAD)
    return title


def add_back(parent, event_cb):
    btn = lv.btn(parent)
    lv.theme_apply(btn, (lv.theme_style_t)LV_DEMO_PRINTER_THEME_BTN_BACK) # TODO:
    btn.set_size(80, 80)
    btn.set_pos(30, 10)
    btn.set_event_cb(event_cb)
    return btn


def add_loader(parent, end_cb):
    arc = lv.arc(parent)
    arc.set_bg_angles(0, 0)
    arc.set_start_angle(270)
    arc.set_size(180, 180)

    a = lv.anim_t()
    a.init()
    a.set_exec_cb(loader_anim_cb)
    a.set_ready_cb(end_cb)
    a.set_values(0, 110)
    a.set_time(2000)
    a.set_var(arc)
    a.start()

    return arc


##### ANIMATIONS #####

def loader_anim_cb(arc, v):
    if v > 100:
        v = 100
    arc.set_end_angle(v * 360 // 100 + 270)

    buf="{} %".format(v)
    arc.set_style_local_value_str(arc.PART.BG, lv.STATE.DEFAULT, buf)


def scan_img_color_refr():
    global scan_img
    global hue_act
    if scan_img:
        s = 100 - lightness_act if lightness_act > 0 else 100
        v = 100 + lightness_act if lightness_act < 0 else 100
        c = lv_color_hsv_to_rgb(hue_act, s, v)
        scan_img.set_style_local_image_recolor(scan_img.PART.MAIN, lv.STATE.DEFAULT, c)


def anim_path_triangle(path, a):
    '''
    Calculate the current value of an animation applying linear characteristic

    Parameters
    ----------
    path : a.path_t
        The animation path
    a : a.t
        Pointer to an animation

    Returns
    ----------
    int:
        The current value to set
    '''
    # Calculate the current step*/
    ret = 0
    if a.time == a.act_time:
        ret = a.end
    else:
        if a.act_time < a.time / 2:
            step = (a.act_time * 1024) // (a.time / 2)
            new_value = step * (LV_DEMO_PRINTER_BG_SMALL - a.start)
            new_value = new_value >> 10
            new_value += a.start
            ret = new_value
        else:
            t = a.act_time - a.time / 2
            step = (t * 1024) // (a.time / 2)
            new_value = step * (a.end - LV_DEMO_PRINTER_BG_SMALL)
            new_value = new_value >> 10
            new_value += LV_DEMO_PRINTER_BG_SMALL

            ret = new_value

    return ret


def lv_demo_printer_anim_bg(bg_top, delay, color, y_new):
    y_act = get_y(bg_top)
    act_color = bg_top.get_style_bg_color(bg_top.PART.MAIN)
    if y_new != LV_DEMO_PRINTER_BG_NORMAL and y_new == y_act and act_color.full == color.full:
        return

    if (y_new == LV_DEMO_PRINTER_BG_NORMAL and y_new == y_act) or (y_new == LV_DEMO_PRINTER_BG_NORMAL and y_act == LV_DEMO_PRINTER_BG_FULL):
        path = a.path_t
        a.path_init(path)
        a.path_set_cb(path, anim_path_triangle(path, a))

        a.init()
        a.set_var(bg_top)
        a.set_time(LV_DEMO_PRINTER_ANIM_TIME_BG + 200)
        a.set_delay(delay)
        a.set_exec_cb((a.exec_xcb_t) set_y)
        a.set_values(y_act, y_new)
        a.set_path(path)
        a.start()
    else:
        a.init()
        a.set_var(bg_top)
        a.set_time(LV_DEMO_PRINTER_ANIM_TIME_BG)
        a.set_delay(delay)
        a.set_exec_cb((a.exec_xcb_t) set_y)
        a.set_values(get_y(bg_top), y_new)
        a.start()

    bg_color_prev = bg_color_act
    bg_color_act = color

    a.set_exec_cb(anim_bg_color_cb)
    a.set_values(0, 255)
    a.set_time(LV_DEMO_PRINTER_ANIM_TIME_BG)
    a.set_path(a.path_def)
    a.start()


def lv_demo_printer_anim_out_all(obj, delay):
    child = obj.get_child_back()
    while child:
        if(child != scan_img && child != bg_top && child != bg_bottom && child != scr)
            a = lv.anim_t()
            a.init()
            a.set_var(child)
            a.set_time(LV_DEMO_PRINTER_ANIM_TIME)
            a.set_delay(delay)
            a.set_exec_cb(set_y)

            if child.get_y() < 80:
                a.set_values(child.get_y(), child.get_y() - LV_DEMO_PRINTER_ANIM_Y)
            else:
                a.set_values(child.get_y(), child.get_y() + LV_DEMO_PRINTER_ANIM_Y)

                delay += LV_DEMO_PRINTER_ANIM_DELAY

            a.set_ready_cb(del_anim_ready_cb)
            a.start()

        child = obj.get_child_back(child)


def lv_demo_printer_anim_in(obj, delay):
    global scan_img
    global bg_top
    global bg_bottom
    global scr
    if obj != bg_top and obj != bg_bottom and obj != scr:
        a = lv.anim_t()
        a.init()
        a.set_var(obj)
        a.set_time(LV_DEMO_PRINTER_ANIM_TIME)
        a.set_delay(delay)
        a.set_exec_cb(set_y)
        a.set_values(obj.get_y() - LV_DEMO_PRINTER_ANIM_Y, obj.get_y())
        a.start()

        fade_in(obj, LV_DEMO_PRINTER_ANIM_TIME - 50, delay)


def anim_bg_color_cb(a, v):
    global bg_color_act
    global bg_color_prev
    global bg_top
    c = lv_color_mix(bg_color_act, bg_color_prev, v)
    bg_top.set_style_local_bg_color(bg_top.PART.MAIN, lv.STATE.DEFAULT, c)

##### MAIN #####

bg_top = None
bg_bottom = None
scan_img = None
print_cnt_label = None
lv_color_t bg_color_prev = None
bg_color_act = None
print_cnt = None
hue_act = None
lightness_act = None
scan_btn_txt = None


bg_color_prev = LV_DEMO_PRINTER_BLUE
bg_color_act = LV_DEMO_PRINTER_BLUE

th = lv.demo_printer_theme_init(LV_COLOR_BLACK, LV_COLOR_BLACK,
        0, &lv_font_montserrat_14, &lv_font_montserrat_22,
        &lv_font_montserrat_28, &lv_font_montserrat_32)
lv.theme_set_act(th)

scr = lv.obj()
lv.scr_load(scr)

bg_top = lv.obj(scr)
scr.clean_style_list(bg_top.PART.MAIN)
scr.set_style_local_bg_opa(bg_top.PART.MAIN, lv.STATE.DEFAULT, lv.OPA.COVER)
scr.set_style_local_bg_color(bg_top.PART.MAIN, lv.STATE.DEFAULT, LV_DEMO_PRINTER_BLUE)
bg_top.set_size(bg_top, LV_HOR_RES, LV_VER_RES)
bg_top.set_y(bg_top, LV_DEMO_PRINTER_BG_NORMAL)

home_open(0)
