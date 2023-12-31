from kivy.uix.label import Label
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineAvatarListItem, ImageLeftWidget, OneLineRightIconListItem, ImageRightWidget
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDTopAppBar


class ViewMtPostScreen(MDScreen):
    def on_enter(self):
        story_app = MDApp.get_running_app()
        com_app = MDApp.get_running_app()

        # Fetch mountain posts
        story_app.cursor.execute("SELECT * FROM posts WHERE location = 'mountain'")
        stories = story_app.cursor.fetchall()

        # Top Navigation Bar
        top_bar = (MDTopAppBar(title="Mountain Bonfire",
                               anchor_title="left",
                               left_action_items=[["home", lambda x: self.callback()]],
                               right_action_items=[["logout", lambda x: self.on_logout()]],
                               elevation=1,
                               md_bg_color=[248 / 255, 143 / 255, 70 / 255, 1],
                               specific_text_color=[44 / 255, 44 / 255, 44 / 255, 1],
                               pos_hint={"top": 1}

                               ))
        # Message Label
        message = MDLabel(text="Check out what people are saying around the Bonfire",
                        pos_hint={"top": 0.85},  # places widget at top of parent
                        size_hint_y=None,
                        valign="top",
                        color=(0, 0, 0, 1),
                        size=(350, 100),  # Forces size of label
                        text_size=(500, None),  # Allows text to wrap
                        padding=(3, 3),
                        halign="center",
                        font_size='19sp'
                        )
        # Scroll View
        scroll = MDScrollView(size_hint=(1, 0.547),
                              pos_hint={"top": 0.7})  # size_hint adjusts the container size of the scroll

        total_layout = MDBoxLayout(orientation='vertical', size_hint_y=None, spacing=20)
        total_layout.bind(minimum_height=total_layout.setter('height'))  # Needed to dynamically add/delete from scrollview

        # Prevent repeats
        self.ids.float.clear_widgets()

        # Displays user stories with like, dislike, and comment buttons
        for i in stories:
            post_id = i[0]
            post_user = i[2]
            post_body = i[3]
            like_counter = self.get_like_count(post_id)
            dislike_counter = self.get_dislike_count(post_id)

            # Display user icon and username
            story_header = OneLineAvatarListItem(ImageLeftWidget(source="posts/img.png"),
                                               text=post_user,
                                               bg_color=(248 / 255, 143 / 255, 70 / 255, 1),
                                           )
            # post content
            story_label = MDLabel(
                text=post_body,
                color=(0, 0, 0, 1),
                size_hint_y=None,
                size=(340, 200),
                text_size=(450, None),  # Allow text wrapping
                padding=(1, 1),
                halign="left",
                valign="top",
            )

            comment_btn = MDRectangleFlatButton(md_bg_color=(248 / 255, 143 / 255, 70 / 255, 0.5),
                                                text="Add Comment",
                                                text_color=(0, 0, 0, 1),
                                                size_hint_y=None,
                                                height=40,
                                                pos_hint={'center_x': 0.5, 'center_y': 0.1},
                                                on_release=(lambda instance, post_id=post_id,
                                                                   post_body=post_body: self.expand_story(post_id,
                                                                                                          post_body))
                                                )
            # Display number of likes
            self.like_label = Label(
                text=f'{like_counter}',
                color=(0, 0, 0, 1),
                size=(20,20),
                pos_hint={'center_x':0.79, 'center_y':1}
            )

            like = MDIconButton(icon="thumb-up",
                                on_release=lambda instance, post=post_id, label=self.like_label: self.like(post, label))

            # Display number of dislikes
            self.dislike_label = Label(
                text=f'{dislike_counter}',
                color=(0, 0, 0, 1),
                size=(20, 20),
                pos_hint={'center_x': 0.93, 'center_y': 1}
            )
            dislike = MDIconButton(icon="thumb-down",
                                   on_release=lambda instance, post=post_id, label=self.dislike_label: self.dislike(post, label))

            like_layout = MDFloatLayout()
            story_layout = MDBoxLayout(orientation="horizontal", size_hint_y=None, spacing=0.5,
                                  md_bg_color=(248 / 255, 143 / 255, 70 / 255, 1),
                                  height=story_header.height
                                  )
            story_layout.add_widget(story_header)
            story_layout.add_widget(like)
            story_layout.add_widget(dislike)

            like_layout.add_widget(self.like_label)
            like_layout.add_widget(self.dislike_label)

            com_app.cursor.execute("SELECT * FROM comments WHERE post_ID = %s", (post_id,))
            comments = com_app.cursor.fetchall()

            com_layout = MDBoxLayout(orientation='vertical', size_hint_y=None)
            com_layout.bind(minimum_height=com_layout.setter('height'))

            # Lists comments to a post underneath the post
            for c in comments:
                com_id = c[1]
                com_user = c[3]
                com_body = c[4]

                com_header = OneLineRightIconListItem(ImageRightWidget(source="posts/img.png"),
                                                   text=com_user,
                                                   bg_color=(248 / 255, 143 / 255, 70 / 255, 0.5))

                com_label = MDLabel(
                    text=com_body,
                    size_hint_y=None,
                    color=(0, 0, 0, 1),
                    size=(300, 300),
                    text_size=(300, None),
                    padding=(5, 5),
                    halign="left",
                    valign="top"
                )

                com_layout.add_widget(com_header)
                com_layout.add_widget(com_label)
            total_layout.add_widget(story_layout)
            total_layout.add_widget(like_layout)

            total_layout.add_widget(story_label)
            total_layout.add_widget(comment_btn)
            total_layout.add_widget(com_layout)

        scroll.add_widget(total_layout)

        add_btn = MDRectangleFlatButton(md_bg_color=(248 / 255, 143 / 255, 70 / 255, 1),
                                        text="Share your story",
                                        text_color=(0, 0, 0, 1),
                                        pos_hint={'center_x': 0.5, 'center_y': 0.1},
                                        on_release=self.add_mt_story
                                        )
        # add everything to parent widget (Float Layout) in .kv file
        self.ids.float.add_widget(top_bar)
        self.ids.float.add_widget(message)
        self.ids.float.add_widget(scroll)
        self.ids.float.add_widget(add_btn)

    def get_like_count(self, post_id):
        # Gets current number of likes for a post
        app = MDApp.get_running_app()
        app.cursor.execute("SELECT likes from posts WHERE post_ID = %s",(post_id,))
        like_sum = app.cursor.fetchone()
        return like_sum[0] if like_sum else 0

    def get_dislike_count(self, post_id):
        # Gets current number of dislikes for a post
        app = MDApp.get_running_app()
        app.cursor.execute("SELECT dislikes from posts WHERE post_ID = %s",(post_id,))
        dislike_sum = app.cursor.fetchone()
        return dislike_sum[0] if dislike_sum else 0

    def like(self, post, label):
        # Increase number of likes by 1
        like_counter = int(label.text)
        like_counter += 1

        app = MDApp.get_running_app()
        sql_command = "UPDATE posts SET likes = %s WHERE post_ID = %s"
        values = (like_counter, post)

        # Execute command
        app.cursor.execute(sql_command, values)

        # Commit changes to database
        app.database.commit()

        label.text = str(like_counter)

        self.on_enter()
        self.manager.current = "ViewMtPostScreen"

    def dislike(self, post, label):
        # Increases number of dislikes by 1
        dislike_counter = int(label.text)
        dislike_counter += 1

        app = MDApp.get_running_app()
        sql_command = "UPDATE posts SET dislikes = %s WHERE post_ID = %s"
        values = (dislike_counter, post)

        # Execute command
        app.cursor.execute(sql_command, values)

        # Commit changes to database
        app.database.commit()

        label.text = str(dislike_counter)

        self.on_enter()
        self.manager.current = "ViewMtPostScreen"

    def add_mt_story(self, touch):
        # Switches to AddCtPostScreen
        self.manager.current = "AddMtPostScreen"


    def expand_story(self, post_id, post_body):
        # Displays dialog box confirming if a user wants to add a comment
        self.dialog = MDDialog(text=f'Story: {post_body}',
                               buttons=[
                                   MDRectangleFlatButton(
                                       text="Add Comment",
                                       pos_hint={"center_x": 0.1, "center_y": 0.5},
                                       on_release=lambda instance, post_id=post_id: self.add_mt_comment(post_id)
                                   ),
                                   MDRectangleFlatButton(
                                       text="Cancel",
                                       pos_hint={"center_x": 0.6, "center_y": 0.5},
                                       on_release=lambda x: self.dialog.dismiss()
                                   )
                               ]
                               )
        self.dialog.open()


    def add_mt_comment(self, post_id):
        # Switches to MtCommentScreen
        self.dialog.dismiss()
        self.manager.get_screen('MtCommentScreen').post_id = post_id
        self.manager.current = "MtCommentScreen"


    def callback(self):
        # Switches back to home page
        self.manager.transition.direction = "right"
        self.manager.current = "MenuScreen"

    def on_logout(self):
        # Switches to LoginScreen and erases any leftover content for username, password, and error text
        login_screen = self.manager.get_screen('LoginScreen')
        login_screen.ids.username.text = ""
        login_screen.ids.password.text = ""
        login_screen.ids.error_label.text = ""
        self.manager.current = 'LoginScreen'
