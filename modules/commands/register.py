from modules import signup, cispr, students
import string
import discord
from discord.commands.context import ApplicationContext


async def register_command(ctx: ApplicationContext, token: str):
    if not cispr.check_token(token):
        await ctx.response.send_message("Your session token didn't work")
        return

    name, id = cispr.get_account_name_and_id(token)
    student = students.from_id(id)
    if student:
        embed = construct_success_embed(student, ctx.user.id)
        await ctx.response.send_message(embed=embed, delete_after=60)
    else:
        all_students = students.search_name(name)
        await ctx.response.send_message(
            view=student_selection(all_students),
            delete_after=60
        )


def student_selection(students: list[students.Student]):
    class StudentSelectView(discord.ui.View):
        @discord.ui.select(
            placeholder="Choose Yourself",
            min_values=1,
            max_values=1,
            options=[
                discord.SelectOption(
                    label=f"{student.name} | {student.id}",
                    description=f"COMP4/{student.seminar_group} {student.email}",
                    value=str(student.id),
                ) for student in students[:10]
            ]
        )
        async def select_callback(self, select, interaction: discord.Interaction):
            student_id = select.values[0]
            selected_student = filter(
                lambda student: str(student.id) == student_id,
                students
            )
            student = next(selected_student)
            embed = construct_success_embed(student, interaction.user.id) # type: ignore
            await interaction.response.send_message(embed=embed, delete_after=60)

    return StudentSelectView()


def construct_success_embed(student: students.Student, discord_id: int) -> discord.Embed:
    embed = discord.Embed(
        title="Sucessfully Signed Up",
        description=f"<@{discord_id}>"
    )
    embed.add_field(name="Name", value=student.name)
    embed.add_field(name="Student Id", value=str(student.id))
    embed.add_field(name="Email", value=student.email)
    embed.add_field(name="Seminar Group", value=f"COMP4/{student.seminar_group}")
    return embed
